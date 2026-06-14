"""Collect links added by a pull request and validate new local paths."""

from argparse import ArgumentParser
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote


MARKDOWN_LINK = re.compile(r"""\]\(([^)\s]+)(?:\s+["'][^)]*["'])?\)""")
HTML_LINK = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
BARE_LINK = re.compile(r"""https?://[^\s<>"']+""")
INLINE_CODE = re.compile(r"`[^`]*`")
EXTERNAL_PREFIXES = ("http://", "https://")
IGNORED_PREFIXES = ("#", "mailto:", "tel:", "data:")
IGNORED_FILES = {Path("docs/stale-links.md")}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--base", required=True, help="Base Git commit to diff")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def added_lines(base):
    result = subprocess.run(
        ["git", "diff", "--unified=0", f"{base}...HEAD", "--", "*.md"],
        check=True,
        capture_output=True,
        text=True,
    )
    current_file = None
    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_file = Path(line[6:])
        elif line.startswith("+") and not line.startswith("+++"):
            yield current_file, line[1:]


def links_in(line):
    found = set()
    code_spans = [match.span() for match in INLINE_CODE.finditer(line)]
    occupied = list(code_spans)

    def in_code_span(match):
        start, end = match.span()
        return any(
            code_start <= start and end <= code_end
            for code_start, code_end in code_spans
        )

    for match in MARKDOWN_LINK.finditer(line):
        if in_code_span(match):
            continue
        found.add(match.group(1))
        occupied.append(match.span())
    for match in HTML_LINK.finditer(line):
        if in_code_span(match):
            continue
        found.add(match.group(1))
        occupied.append(match.span())

    bare_text = list(line)
    for start, end in occupied:
        bare_text[start:end] = " " * (end - start)
    for match in BARE_LINK.finditer("".join(bare_text)):
        found.add(match.group(0).rstrip(".,;:)]}"))
    yield from found


def normalize(raw_link):
    link = raw_link.strip().strip("<>")
    if " " in link and not link.startswith(EXTERNAL_PREFIXES):
        link = link.split(" ", 1)[0]
    return link


def main():
    args = parse_args()
    external_links = set()
    broken_local_links = []

    for source_file, line in added_lines(args.base):
        if source_file is None or source_file in IGNORED_FILES:
            continue
        for raw_link in links_in(line):
            link = normalize(raw_link)
            if not link or link.startswith(IGNORED_PREFIXES):
                continue
            if link.startswith(EXTERNAL_PREFIXES):
                external_links.add(link)
                continue

            path = unquote(link.split("#", 1)[0])
            if not path:
                continue
            target = Path(path.lstrip("/")) if path.startswith("/") else source_file.parent / path
            if not target.exists():
                broken_local_links.append(f"{source_file}: {link}")

    if broken_local_links:
        details = "\n".join(f"- {item}" for item in broken_local_links)
        raise SystemExit(f"New local links do not resolve:\n{details}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# New external links", ""]
    lines.extend(f"- <{link}>" for link in sorted(external_links))
    if not external_links:
        lines.append("No new external links in this pull request.")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Collected {len(external_links)} new external link(s).")


if __name__ == "__main__":
    main()
