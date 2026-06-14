import re

with open("webapp/test/README-redesign.md", "r") as f:
    content = f.read()

replacements = {
    "docs/assets/dsai-gate-hero.svg": "../assets/dsai-gate-hero.svg",
    "PYQ/README.md": "../../PYQ/README.md",
    "notebooks/README.md": "../../notebooks/README.md",
    "LICENSE": "../../LICENSE",
    "Probability-Statistics-Readme.md": "../../Probability-Statistics-Readme.md",
    "Linear-Algebra-Readme.md": "../../Linear-Algebra-Readme.md",
    "Calculus-and-Optimization-Readme.md": "../../Calculus-and-Optimization-Readme.md",
    "Programming-and-Algorithms-Readme.md": "../../Programming-and-Algorithms-Readme.md",
    "Database-Management-Readme.md": "../../Database-Management-Readme.md",
    "Machine-Learning-Readme.md": "../../Machine-Learning-Readme.md",
    "Artificial-Intelligence-Readme.md": "../../Artificial-Intelligence-Readme.md",
    "docs/official-resources.md": "../../docs/official-resources.md",
    "docs/agent.md": "../../docs/agent.md",
    "docs/implementation_plan.md": "../../docs/implementation_plan.md",
    "docs/future_directions.md": "../../docs/future_directions.md",
    "docs/stale-links.md": "../../docs/stale-links.md",
}

for old, new in replacements.items():
    content = re.sub(r'href="' + old + r'"', r'href="' + new + '"', content)
    content = re.sub(r'href="' + old + r'#([^"]*)"', r'href="' + new + r'#\1"', content)
    content = re.sub(r'src="' + old + r'"', r'src="' + new + '"', content)
    # Also handle markdown links [text](link)
    # We need to escape old strings with dots
    escaped_old = old.replace(".", r"\.")
    content = re.sub(r'\]\(' + escaped_old + r'\)', r'](' + new + ')', content)

with open("webapp/test/README-redesign.md", "w") as f:
    f.write(content)
