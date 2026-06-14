const storageKey = "dsai-gate-progress-v1";
const notesKey = "dsai-gate-notes-v1";
const themeKey = "dsai-gate-theme";

const subjects = JSON.parse(document.querySelector("#syllabus-data").textContent);
const slides = subjects.flatMap((subject) =>
  subject.topics.map((topic, index) => ({
    id: `${subject.id}:${index}`,
    topic,
    subject,
  })),
);

const topicInputs = [...document.querySelectorAll("[data-topic]")];
const subjectCards = [...document.querySelectorAll("[data-subject-card]")];
const subjectButtons = [...document.querySelectorAll("[data-subject]")];
const chips = [...document.querySelectorAll("[data-filter]")];
const searchInput = document.querySelector("#search-input");
const emptyState = document.querySelector("#empty-state");
const sidebar = document.querySelector("#sidebar");
const presentation = document.querySelector("#presentation");
const presentationStage = document.querySelector(".presentation-stage");
const studySlide = document.querySelector("#study-slide");
const overallMapPanel = document.querySelector("#overall-map-panel");
const focusTab = document.querySelector("#focus-tab");
const overallMapTab = document.querySelector("#overall-map-tab");
const notesPanel = document.querySelector("#notes-panel");
const notesInput = document.querySelector("#notes-input");

let currentFilter = "all";
let currentSlide = 0;
let currentPresentationView = "focus";
let progress = loadStored(storageKey);
let notes = loadStored(notesKey);
let noteSaveTimer;

function loadStored(key) {
  try {
    return JSON.parse(localStorage.getItem(key)) || {};
  } catch {
    return {};
  }
}

function saveStored(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function syncInputs() {
  topicInputs.forEach((input) => {
    input.checked = Boolean(progress[input.dataset.topic]);
  });
}

function updateProgress() {
  let completed = 0;

  subjectCards.forEach((card) => {
    const id = card.dataset.subjectCard;
    const inputs = [...card.querySelectorAll("[data-topic]")];
    const done = inputs.filter((input) => input.checked).length;
    const percent = inputs.length ? Math.round((done / inputs.length) * 100) : 0;
    completed += done;

    document.querySelector(`[data-progress="${id}"]`).textContent = `${done}/${inputs.length}`;
    document.querySelector(`[data-card-progress="${id}"]`).textContent = `${percent}%`;
    document.querySelector(`[data-card-bar="${id}"]`).style.width = `${percent}%`;
  });

  const total = topicInputs.length;
  const percent = total ? Math.round((completed / total) * 100) : 0;
  document.querySelector("#completed-count").textContent = completed;
  document.querySelector("#overall-percent").textContent = `${percent}%`;
  document.querySelector("#overall-bar").style.width = `${percent}%`;
}

function applyFilters() {
  const query = searchInput.value.trim().toLowerCase();
  let visibleTopics = 0;

  subjectCards.forEach((card) => {
    let cardHasVisibleTopic = false;
    card.querySelectorAll("[data-topic-row]").forEach((row) => {
      const input = row.querySelector("[data-topic]");
      const matchesQuery = !query || row.dataset.topicText.includes(query);
      const matchesProgress =
        currentFilter === "all" ||
        (currentFilter === "complete" && input.checked) ||
        (currentFilter === "open" && !input.checked);
      const visible = matchesQuery && matchesProgress;
      row.hidden = !visible;
      cardHasVisibleTopic ||= visible;
      visibleTopics += Number(visible);
    });
    card.hidden = !cardHasVisibleTopic;
  });

  emptyState.hidden = visibleTopics !== 0;
}

function selectSubject(id) {
  subjectButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.subject === id);
  });
}

function toggleFullscreen() {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    document.documentElement.requestFullscreen();
  }
}

function openPresentation(index = 0) {
  currentSlide = Math.min(Math.max(index, 0), slides.length - 1);
  presentation.hidden = false;
  document.body.classList.add("presentation-open");
  setPresentationView("focus");
  renderSlide();
  history.replaceState(null, "", `#present=${currentSlide}`);
}

function closePresentation() {
  presentation.hidden = true;
  notesPanel.hidden = true;
  document.body.classList.remove("presentation-open");
  history.replaceState(null, "", `${location.pathname}${location.search}`);
}

function slideLink(label, url) {
  const link = document.createElement("a");
  link.href = url;
  link.target = "_blank";
  link.rel = "noreferrer";
  link.textContent = `${label} ↗`;
  return link;
}

function resourceNode(resource) {
  const link = document.createElement("a");
  const kind = document.createElement("span");
  const title = document.createElement("strong");
  const detail = document.createElement("span");
  link.href = resource.url;
  link.target = "_blank";
  link.rel = "noreferrer";
  link.className = "resource-node";
  link.dataset.relevance = resource.relevance;
  kind.className = "resource-kind";
  kind.textContent = resource.kind;
  title.textContent = resource.title;
  detail.textContent = resource.relevance === "topic" ? "Matched to this topic ↗" : "Broader subject resource ↗";
  link.append(kind, title, detail);
  return link;
}

function escapeMermaid(value) {
  return value.replaceAll("&", "and").replaceAll("\\", "\\\\").replaceAll('"', "'");
}

function resourceMapDefinition(slide, topicMap) {
  const lines = [
    "flowchart LR",
    `topic["${escapeMermaid(slide.topic)}"]`,
  ];
  topicMap.related.forEach((topic, index) => {
    lines.push(`concept${index}["${escapeMermaid(topic)}"]`);
    lines.push(`concept${index} --- topic`);
  });
  topicMap.resources.forEach((resource, index) => {
    lines.push(`resource${index}["${escapeMermaid(resource.kind)}<br/>${escapeMermaid(resource.title)}"]`);
    lines.push(`topic --> resource${index}`);
    lines.push(`click resource${index} "${escapeMermaid(resource.url)}" "Open curated resource"`);
    lines.push(`class resource${index} ${resource.relevance === "topic" ? "matched" : "broader"}`);
  });
  lines.push(
    "classDef current fill:#312e81,stroke:#a78bfa,color:#ffffff,stroke-width:3px",
    "classDef concept fill:#172033,stroke:#58c4dd,color:#ffffff,stroke-width:2px",
    "classDef matched fill:#172033,stroke:#22c55e,color:#ffffff,stroke-width:2px",
    "classDef broader fill:#172033,stroke:#64748b,color:#cbd5e1,stroke-width:1px",
    "class topic current",
  );
  if (topicMap.related.length) {
    lines.push(`class ${topicMap.related.map((_, index) => `concept${index}`).join(",")} concept`);
  }
  return lines.join("\n");
}

function overallMapDefinition() {
  const lines = [
    "mindmap",
    '  root(("GATE DA"))',
  ];
  subjects.forEach((subject, subjectIndex) => {
    lines.push(`    subject${subjectIndex}["${escapeMermaid(subject.title)}"]`);
    subject.topics.forEach((topic, topicIndex) => {
      lines.push(`      topic${subjectIndex}_${topicIndex}["${escapeMermaid(topic)}"]`);
    });
  });
  return lines.join("\n");
}

function renderOverallMapFallback(map) {
  const grid = document.createElement("div");
  grid.className = "overall-map-fallback";
  subjects.forEach((subject) => {
    const section = document.createElement("section");
    const title = document.createElement("h3");
    const topics = document.createElement("ul");
    title.textContent = subject.title;
    subject.topics.forEach((topic) => {
      const item = document.createElement("li");
      item.textContent = topic;
      topics.append(item);
    });
    section.append(title, topics);
    grid.append(section);
  });
  map.replaceChildren(grid);
}

async function renderOverallMap() {
  const map = document.querySelector("#overall-map");
  if (map.dataset.rendered === "true") return;
  if (!window.mermaid) {
    renderOverallMapFallback(map);
    return;
  }
  try {
    const { svg, bindFunctions } = await window.mermaid.render("overall-memory-map-svg", overallMapDefinition());
    map.innerHTML = svg;
    bindFunctions?.(map);
    map.dataset.rendered = "true";
  } catch {
    renderOverallMapFallback(map);
  }
}

function setPresentationView(view, updateHistory = true) {
  currentPresentationView = view;
  const showingOverall = view === "overall";
  studySlide.hidden = showingOverall;
  overallMapPanel.hidden = !showingOverall;
  document.querySelector("#slide-previous").hidden = showingOverall;
  document.querySelector("#slide-next").hidden = showingOverall;
  focusTab.classList.toggle("active", !showingOverall);
  overallMapTab.classList.toggle("active", showingOverall);
  focusTab.setAttribute("aria-selected", String(!showingOverall));
  overallMapTab.setAttribute("aria-selected", String(showingOverall));
  document.querySelector("#presentation-mode-title").textContent = showingOverall ? "Memory map" : "Focus mode";
  document.querySelector("#slide-counter").textContent = showingOverall ? `${subjects.length} subjects · ${slides.length} topics` : `${currentSlide + 1} / ${slides.length}`;
  presentationStage.scrollTo({ top: 0, left: 0 });
  if (showingOverall) renderOverallMap();
  if (updateHistory && !presentation.hidden) {
    history.replaceState(null, "", showingOverall ? "#map" : `#present=${currentSlide}`);
  }
}

function conceptNode(topic, current) {
  const node = document.createElement("button");
  node.className = current ? "concept-node current" : "concept-node";
  node.textContent = topic;
  if (!current) {
    const index = slides.findIndex((slide) => slide.topic === topic);
    if (index >= 0) {
      node.addEventListener("click", () => openPresentation(index));
    } else {
      node.disabled = true;
    }
  }
  return node;
}

function renderResourceMapFallback(map, slide, topicMap) {
  const concepts = document.createElement("div");
  const resources = document.createElement("div");
  concepts.className = "concept-branch";
  resources.className = "resource-branch";
  concepts.append(conceptNode(slide.topic, true), ...topicMap.related.map((topic) => conceptNode(topic, false)));
  resources.append(...topicMap.resources.map(resourceNode));
  map.replaceChildren(concepts, resources);
}

async function renderResourceMap(slide) {
  const map = document.querySelector("#resource-map");
  const topicMap = slide.subject.topic_maps[slide.subject.topics.indexOf(slide.topic)];
  if (!window.mermaid) {
    renderResourceMapFallback(map, slide, topicMap);
    return;
  }
  try {
    const id = `resource-map-svg-${slide.id.replaceAll(":", "-")}`;
    const { svg, bindFunctions } = await window.mermaid.render(id, resourceMapDefinition(slide, topicMap));
    map.innerHTML = svg;
    bindFunctions?.(map);
  } catch {
    renderResourceMapFallback(map, slide, topicMap);
  }
}

function renderSlide() {
  const slide = slides[currentSlide];
  const links = document.querySelector("#slide-links");
  presentationStage.scrollTo({ top: 0, left: 0 });
  if (currentPresentationView === "focus") {
    document.querySelector("#slide-counter").textContent = `${currentSlide + 1} / ${slides.length}`;
  }
  document.querySelector("#slide-subject").textContent = `${slide.subject.number} · ${slide.subject.title}`;
  document.querySelector("#slide-title").textContent = slide.topic;
  document.querySelector("#slide-description").textContent = slide.subject.description;
  document.querySelector("#notes-title").textContent = slide.topic;
  notesInput.value = notes[slide.id] || "";
  links.replaceChildren(slideLink("Study guide", slide.subject.guide));
  if (slide.subject.notebook) links.append(slideLink("Notebook", slide.subject.notebook));
  renderResourceMap(slide);
  document.querySelector("#slide-previous").disabled = currentSlide === 0;
  document.querySelector("#slide-next").disabled = currentSlide === slides.length - 1;
  history.replaceState(null, "", `#present=${currentSlide}`);
}

function moveSlide(direction) {
  const next = currentSlide + direction;
  if (next >= 0 && next < slides.length) {
    currentSlide = next;
    renderSlide();
  }
}

function toggleNotes(force) {
  notesPanel.hidden = force === undefined ? !notesPanel.hidden : !force;
  if (!notesPanel.hidden) notesInput.focus();
}

function saveNote(id, value) {
  notes[id] = value;
  saveStored(notesKey, notes);
  document.querySelector("#notes-status").textContent = "Saved locally";
}

function exportNotes() {
  const body = slides
    .filter((slide) => notes[slide.id]?.trim())
    .map((slide) => `## ${slide.subject.title}: ${slide.topic}\n\n${notes[slide.id].trim()}`)
    .join("\n\n");
  const content = `# DSAI-GATE Study Notes\n\n${body || "No notes yet."}\n`;
  const download = document.createElement("a");
  download.href = URL.createObjectURL(new Blob([content], { type: "text/markdown" }));
  download.download = "dsai-gate-study-notes.md";
  download.click();
  URL.revokeObjectURL(download.href);
}

topicInputs.forEach((input) => {
  input.addEventListener("change", () => {
    progress[input.dataset.topic] = input.checked;
    saveStored(storageKey, progress);
    updateProgress();
    applyFilters();
  });
});

subjectButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.subject;
    selectSubject(id);
    document.querySelector(`#${id}`).scrollIntoView({ behavior: "smooth", block: "start" });
    sidebar.classList.remove("open");
  });
});

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    currentFilter = chip.dataset.filter;
    chips.forEach((item) => item.classList.toggle("active", item === chip));
    applyFilters();
  });
});

document.querySelectorAll("[data-open-topic]").forEach((button) => {
  button.addEventListener("click", () => openPresentation(slides.findIndex((slide) => slide.id === button.dataset.openTopic)));
});

document.querySelectorAll("[data-present-subject]").forEach((button) => {
  button.addEventListener("click", () => openPresentation(slides.findIndex((slide) => slide.subject.id === button.dataset.presentSubject)));
});

document.querySelectorAll("[data-present-start]").forEach((button) => {
  button.addEventListener("click", () => openPresentation(Number(button.dataset.presentStart)));
});

searchInput.addEventListener("input", applyFilters);

document.addEventListener("keydown", (event) => {
  if (!presentation.hidden && document.activeElement !== notesInput) {
    if (event.key === "ArrowLeft") moveSlide(-1);
    if (event.key === "ArrowRight") moveSlide(1);
    if (event.key.toLowerCase() === "n") toggleNotes();
    if (event.key.toLowerCase() === "f") toggleFullscreen();
    if (event.key === "Escape") closePresentation();
    return;
  }
  if (event.key === "/" && document.activeElement !== searchInput) {
    event.preventDefault();
    searchInput.focus();
  }
});

document.querySelectorAll("[data-scroll-to]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector(`#${button.dataset.scrollTo}`).scrollIntoView({ behavior: "smooth" });
  });
});

document.querySelector("#menu-toggle").addEventListener("click", () => sidebar.classList.add("open"));
document.querySelector("#menu-close").addEventListener("click", () => sidebar.classList.remove("open"));
document.querySelector("#fullscreen-toggle").addEventListener("click", toggleFullscreen);
document.querySelector("#presentation-fullscreen").addEventListener("click", toggleFullscreen);
document.querySelector("#present-all").addEventListener("click", () => openPresentation(0));
document.querySelector("#presentation-close").addEventListener("click", closePresentation);
focusTab.addEventListener("click", () => {
  setPresentationView("focus");
  renderSlide();
});
overallMapTab.addEventListener("click", () => setPresentationView("overall"));
document.querySelector("#slide-previous").addEventListener("click", () => moveSlide(-1));
document.querySelector("#slide-next").addEventListener("click", () => moveSlide(1));
document.querySelector("#slide-notes-toggle").addEventListener("click", () => toggleNotes());
document.querySelector("#notes-close").addEventListener("click", () => toggleNotes(false));
document.querySelector("#notes-export").addEventListener("click", exportNotes);

notesInput.addEventListener("input", () => {
  document.querySelector("#notes-status").textContent = "Saving...";
  clearTimeout(noteSaveTimer);
  const id = slides[currentSlide].id;
  const value = notesInput.value;
  noteSaveTimer = setTimeout(() => saveNote(id, value), 250);
});

const themeToggle = document.querySelector("#theme-toggle");
const preferredTheme =
  localStorage.getItem(themeKey) ||
  (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
document.body.classList.toggle("dark", preferredTheme === "dark");
window.mermaid?.initialize({ startOnLoad: false, securityLevel: "loose", theme: preferredTheme === "dark" ? "dark" : "neutral" });

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem(themeKey, document.body.classList.contains("dark") ? "dark" : "light");
});

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) selectSubject(visible.target.dataset.subjectCard);
  },
  { rootMargin: "-20% 0px -65% 0px", threshold: [0.1, 0.35] },
);
subjectCards.forEach((card) => observer.observe(card));

syncInputs();
updateProgress();
applyFilters();

const presentMatch = location.hash.match(/^#present=(\d+)$/);
if (location.hash === "#map") {
  presentation.hidden = false;
  document.body.classList.add("presentation-open");
  setPresentationView("overall");
} else if (presentMatch) {
  openPresentation(Number(presentMatch[1]));
}
