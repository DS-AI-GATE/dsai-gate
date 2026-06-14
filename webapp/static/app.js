const storageKey = "dsai-gate-progress-v1";
const notesKey = "dsai-gate-notes-v1";
const themeKey = "dsai-gate-theme";
const customMapNodesKey = "dsai-gate-custom-map-nodes-v1";

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
let customMapNodes = loadStored(customMapNodesKey);
let noteSaveTimer;
let selectedCustomNodeId = null;
if (!Array.isArray(customMapNodes)) customMapNodes = [];

const mapColors = [
  { branch: "#9f6674", soft: "#f4e4e8", text: "#633642", foreground: "#ffffff" },
  { branch: "#79a7a3", soft: "#e3f0ee", text: "#355f5c", foreground: "#173f3c" },
  { branch: "#c29a62", soft: "#f5ead8", text: "#715126", foreground: "#4d3414" },
  { branch: "#82a986", soft: "#e6f0e5", text: "#416546", foreground: "#214727" },
  { branch: "#b7836e", soft: "#f3e4de", text: "#704636", foreground: "#4f2c20" },
  { branch: "#ae7898", soft: "#f2e3ec", text: "#6c3f59", foreground: "#ffffff" },
  { branch: "#8586ae", soft: "#e9e8f2", text: "#4d4e76", foreground: "#ffffff" },
];

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
  const subjectIndex = subjects.findIndex((subject) => subject.id === slide.subject.id);
  const color = mapColors[subjectIndex] || mapColors[0];
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
    `classDef current fill:${color.branch},stroke:${color.text},color:${color.foreground},stroke-width:3px`,
    `classDef concept fill:${color.soft},stroke:${color.branch},color:${color.text},stroke-width:2px`,
    "classDef matched fill:#dcfce7,stroke:#22c55e,color:#166534,stroke-width:2px",
    "classDef broader fill:#f1f5f9,stroke:#64748b,color:#334155,stroke-width:1px",
    "class topic current",
  );
  if (topicMap.related.length) {
    lines.push(`class ${topicMap.related.map((_, index) => `concept${index}`).join(",")} concept`);
  }
  return lines.join("\n");
}

const svgNamespace = "http://www.w3.org/2000/svg";

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(svgNamespace, name);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  return element;
}

function radialPoint(center, radius, angle) {
  return {
    x: center.x + Math.cos(angle) * radius,
    y: center.y + Math.sin(angle) * radius,
  };
}

function radialNode({ id, x, y, width, label, fill, stroke, color, className, activate }) {
  const words = label.split(/\s+/);
  const lines = [];
  let line = "";
  words.forEach((word) => {
    if (`${line} ${word}`.trim().length > 22 && line) {
      lines.push(line);
      line = word;
    } else {
      line = `${line} ${word}`.trim();
    }
  });
  if (line) lines.push(line);

  const height = Math.max(44, lines.length * 15 + 20);
  const group = svgElement("g", {
    class: `radial-node${activate ? " map-link" : ""} ${className}`,
    transform: `translate(${x - width / 2} ${y - height / 2})`,
    "data-node-id": id,
    "data-x": x,
    "data-y": y,
    "data-width": width,
    "data-height": height,
  });
  if (activate) {
    group.setAttribute("role", "link");
    group.setAttribute("tabindex", "0");
    group.setAttribute("aria-label", label);
  }
  group.append(svgElement("rect", {
    width,
    height,
    rx: className === "root-node" ? height / 2 : 10,
    fill,
    stroke,
  }));
  const text = svgElement("text", {
    x: width / 2,
    y: height / 2 - ((lines.length - 1) * 7),
    fill: color,
    "text-anchor": "middle",
  });
  lines.forEach((textLine, index) => {
    const span = svgElement("tspan", {
      x: width / 2,
      dy: index === 0 ? "0" : "15",
    });
    span.textContent = textLine;
    text.append(span);
  });
  group.append(text);
  if (activate) {
    group.addEventListener("click", activate);
    group.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activate();
      }
    });
  }
  return group;
}

function enableMapInteractions(map, svg, viewport) {
  const state = { scale: 1, x: 0, y: 0 };
  let interaction = null;
  let suppressClick = false;

  const applyViewport = () => {
    viewport.setAttribute("transform", `translate(${state.x} ${state.y}) scale(${state.scale})`);
    map.style.setProperty("--map-zoom", `${Math.round(state.scale * 100)}%`);
  };
  const svgPoint = (event) => {
    const point = svg.createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    return point.matrixTransform(svg.getScreenCTM().inverse());
  };
  const graphPoint = (event) => {
    const point = svgPoint(event);
    return {
      x: (point.x - state.x) / state.scale,
      y: (point.y - state.y) / state.scale,
    };
  };
  const updateNode = (node, x, y) => {
    const width = Number(node.dataset.width);
    const height = Number(node.dataset.height);
    node.dataset.x = x;
    node.dataset.y = y;
    node.setAttribute("transform", `translate(${x - width / 2} ${y - height / 2})`);
    viewport.querySelectorAll(`[data-from="${node.dataset.nodeId}"]`).forEach((edge) => {
      edge.setAttribute("x1", x);
      edge.setAttribute("y1", y);
    });
    viewport.querySelectorAll(`[data-to="${node.dataset.nodeId}"]`).forEach((edge) => {
      edge.setAttribute("x2", x);
      edge.setAttribute("y2", y);
    });
    if (node.dataset.custom === "true") {
      const savedNode = customMapNodes.find((item) => item.id === node.dataset.nodeId);
      if (savedNode) {
        savedNode.x = x;
        savedNode.y = y;
        document.querySelector("#map-save-status").textContent = "Move pending...";
      }
    }
  };
  const zoomAt = (factor, anchor = { x: 950, y: 725 }) => {
    const nextScale = Math.min(3, Math.max(0.4, state.scale * factor));
    const graphX = (anchor.x - state.x) / state.scale;
    const graphY = (anchor.y - state.y) / state.scale;
    state.x = anchor.x - graphX * nextScale;
    state.y = anchor.y - graphY * nextScale;
    state.scale = nextScale;
    applyViewport();
  };
  const reset = () => {
    state.scale = 1;
    state.x = 0;
    state.y = 0;
    applyViewport();
  };
  const selectCustomNode = (node) => {
    viewport.querySelectorAll(".custom-node.selected").forEach((item) => item.classList.remove("selected"));
    selectedCustomNodeId = node?.dataset.custom === "true" ? node.dataset.nodeId : null;
    if (selectedCustomNodeId) {
      node.classList.add("selected");
      document.querySelector("#map-save-status").textContent = "Selected node. Press Delete to remove it.";
    }
  };

  svg.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    const node = event.target.closest(".radial-node");
    selectCustomNode(node);
    const point = node ? graphPoint(event) : svgPoint(event);
    interaction = {
      type: node ? "node" : "pan",
      node,
      start: point,
      originX: node ? Number(node.dataset.x) : state.x,
      originY: node ? Number(node.dataset.y) : state.y,
      moved: false,
    };
    svg.setPointerCapture(event.pointerId);
    svg.classList.add("interacting");
    node?.classList.add("dragging");
  });
  svg.addEventListener("pointermove", (event) => {
    if (!interaction) return;
    const point = interaction.type === "node" ? graphPoint(event) : svgPoint(event);
    const dx = point.x - interaction.start.x;
    const dy = point.y - interaction.start.y;
    interaction.moved ||= Math.hypot(dx, dy) > 3;
    if (interaction.type === "node") {
      updateNode(interaction.node, interaction.originX + dx, interaction.originY + dy);
    } else {
      state.x = interaction.originX + dx;
      state.y = interaction.originY + dy;
      applyViewport();
    }
  });
  const endInteraction = (event) => {
    if (!interaction) return;
    suppressClick = interaction.moved;
    if (interaction.moved && interaction.node?.dataset.custom === "true") {
      saveStored(customMapNodesKey, customMapNodes);
      document.querySelector("#map-save-status").textContent = "Position saved";
    }
    interaction.node?.classList.remove("dragging");
    interaction = null;
    svg.classList.remove("interacting");
    if (svg.hasPointerCapture(event.pointerId)) svg.releasePointerCapture(event.pointerId);
  };
  svg.addEventListener("pointerup", endInteraction);
  svg.addEventListener("pointercancel", endInteraction);
  svg.addEventListener("click", (event) => {
    if (!suppressClick) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    suppressClick = false;
  }, true);
  svg.addEventListener("wheel", (event) => {
    event.preventDefault();
    zoomAt(event.deltaY < 0 ? 1.12 : 1 / 1.12, svgPoint(event));
  }, { passive: false });

  document.querySelector("#map-zoom-in").onclick = () => zoomAt(1.2);
  document.querySelector("#map-zoom-out").onclick = () => zoomAt(1 / 1.2);
  document.querySelector("#map-reset").onclick = reset;
  reset();
}

function renderRadialOverallMap(map) {
  const width = 1900;
  const height = 1450;
  const center = { x: width / 2, y: height / 2 };
  const subjectRadius = 300;
  const topicRadii = [520, 680];
  const sectorWidth = (Math.PI * 2) / subjects.length;
  const svg = svgElement("svg", {
    id: "overall-memory-map-svg",
    class: "radial-memory-map",
    viewBox: `0 0 ${width} ${height}`,
    role: "graphics-document",
    "aria-label": "GATE DA syllabus radial memory map",
  });
  const viewport = svgElement("g", { class: "radial-viewport" });
  const edges = svgElement("g", { class: "radial-edges" });
  const nodes = svgElement("g", { class: "radial-nodes" });
  const rootId = "root";
  const positions = new Map([[rootId, center]]);
  const nodeColors = new Map([[rootId, mapColors[0]]]);

  subjects.forEach((subject, subjectIndex) => {
    const color = mapColors[subjectIndex] || mapColors[0];
    const subjectAngle = -Math.PI / 2 + subjectIndex * sectorWidth;
    const subjectPoint = radialPoint(center, subjectRadius, subjectAngle);
    positions.set(subject.id, subjectPoint);
    nodeColors.set(subject.id, color);
    edges.append(svgElement("line", {
      x1: center.x,
      y1: center.y,
      x2: subjectPoint.x,
      y2: subjectPoint.y,
      stroke: color.branch,
      class: "root-edge",
      "data-from": rootId,
      "data-to": subject.id,
    }));

    const firstRingCount = Math.ceil(subject.topics.length / 2);
    subject.topics.forEach((topic, topicIndex) => {
      const ringIndex = topicIndex < firstRingCount ? 0 : 1;
      const ringTopics = ringIndex === 0
        ? subject.topics.slice(0, firstRingCount)
        : subject.topics.slice(firstRingCount);
      const position = ringIndex === 0 ? topicIndex : topicIndex - firstRingCount;
      const spread = sectorWidth * 0.72;
      const topicAngle = subjectAngle + (
        ringTopics.length === 1 ? 0 : -spread / 2 + (spread * position) / (ringTopics.length - 1)
      );
      const topicPoint = radialPoint(center, topicRadii[ringIndex], topicAngle);
      positions.set(`${subject.id}:${topicIndex}`, topicPoint);
      nodeColors.set(`${subject.id}:${topicIndex}`, color);
      edges.append(svgElement("line", {
        x1: subjectPoint.x,
        y1: subjectPoint.y,
        x2: topicPoint.x,
        y2: topicPoint.y,
        stroke: color.branch,
        class: "topic-edge",
        "data-from": subject.id,
        "data-to": `${subject.id}:${topicIndex}`,
      }));
      const slideIndex = slides.findIndex(
        (slide) => slide.subject.id === subject.id && slide.topic === topic,
      );
      nodes.append(radialNode({
        id: `${subject.id}:${topicIndex}`,
        ...topicPoint,
        width: 170,
        label: topic,
        fill: color.soft,
        stroke: color.branch,
        color: color.text,
        className: "topic-node",
        activate: () => {
          setPresentationView("focus", false);
          currentSlide = slideIndex;
          renderSlide();
        },
      }));
    });

    nodes.append(radialNode({
      id: subject.id,
      ...subjectPoint,
      width: 190,
      label: subject.title,
      fill: color.branch,
      stroke: color.text,
      color: color.foreground,
      className: "subject-node",
      activate: () => window.open(subject.guide, "_blank", "noopener,noreferrer"),
    }));
  });

  nodes.append(radialNode({
    id: rootId,
    ...center,
    width: 120,
    label: "GATE DA",
    fill: "#312e81",
    stroke: "#a78bfa",
    color: "#ffffff",
    className: "root-node",
  }));
  customMapNodes.forEach((customNode, index) => {
    const parentPoint = positions.get(customNode.parentId) || center;
    const color = nodeColors.get(customNode.parentId) || mapColors[index % mapColors.length];
    const angle = index * 2.399963229728653;
    const x = Number.isFinite(customNode.x) ? customNode.x : parentPoint.x + Math.cos(angle) * 190;
    const y = Number.isFinite(customNode.y) ? customNode.y : parentPoint.y + Math.sin(angle) * 190;
    customNode.x = x;
    customNode.y = y;
    positions.set(customNode.id, { x, y });
    nodeColors.set(customNode.id, color);
    edges.append(svgElement("line", {
      x1: parentPoint.x,
      y1: parentPoint.y,
      x2: x,
      y2: y,
      stroke: color.branch,
      class: "custom-edge topic-edge",
      "data-from": customNode.parentId,
      "data-to": customNode.id,
    }));
    const node = radialNode({
      id: customNode.id,
      x,
      y,
      width: 170,
      label: customNode.title,
      fill: "#fff7d6",
      stroke: color.branch,
      color: "#57450c",
      className: "custom-node",
      activate: customNode.url
        ? () => window.open(customNode.url, "_blank", "noopener,noreferrer")
        : undefined,
    });
    node.dataset.custom = "true";
    if (customNode.id === selectedCustomNodeId) node.classList.add("selected");
    nodes.append(node);
  });
  saveStored(customMapNodesKey, customMapNodes);
  viewport.append(edges, nodes);
  svg.append(viewport);
  map.replaceChildren(svg);
  enableMapInteractions(map, svg, viewport);
  map.dataset.rendered = "true";
}

function populateMapParentOptions() {
  const select = document.querySelector("#map-node-parent");
  const options = [{ id: "root", label: "GATE DA" }];
  subjects.forEach((subject) => {
    options.push({ id: subject.id, label: subject.title });
    subject.topics.forEach((topic, index) => {
      options.push({ id: `${subject.id}:${index}`, label: `${subject.short} · ${topic}` });
    });
  });
  customMapNodes.forEach((node) => {
    options.push({ id: node.id, label: `Custom · ${node.title}` });
  });
  select.replaceChildren(...options.map((option) => {
    const element = document.createElement("option");
    element.value = option.id;
    element.textContent = option.label;
    return element;
  }));
}

function deleteSelectedCustomNode() {
  if (!selectedCustomNodeId) return;
  const deleting = new Set([selectedCustomNodeId]);
  let foundDescendant = true;
  while (foundDescendant) {
    foundDescendant = false;
    customMapNodes.forEach((node) => {
      if (deleting.has(node.parentId) && !deleting.has(node.id)) {
        deleting.add(node.id);
        foundDescendant = true;
      }
    });
  }
  customMapNodes = customMapNodes.filter((node) => !deleting.has(node.id));
  selectedCustomNodeId = null;
  saveStored(customMapNodesKey, customMapNodes);
  populateMapParentOptions();
  document.querySelector("#map-save-status").textContent = `${deleting.size} node${deleting.size === 1 ? "" : "s"} deleted`;
  rerenderOverallMap();
}

function rerenderOverallMap() {
  const map = document.querySelector("#overall-map");
  map.dataset.rendered = "false";
  renderOverallMap();
}

function renderOverallMapFallback(map) {
  const grid = document.createElement("div");
  grid.className = "overall-map-fallback";
  subjects.forEach((subject, subjectIndex) => {
    const section = document.createElement("section");
    const title = document.createElement("h3");
    const topics = document.createElement("ul");
    section.style.setProperty("--map-color", (mapColors[subjectIndex] || mapColors[0]).branch);
    section.style.setProperty("--map-soft-color", (mapColors[subjectIndex] || mapColors[0]).soft);
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
  try {
    renderRadialOverallMap(map);
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
  const subjectIndex = subjects.findIndex((subject) => subject.id === slide.subject.id);
  const color = mapColors[subjectIndex] || mapColors[0];
  map.style.setProperty("--map-color", color.branch);
  map.style.setProperty("--map-soft-color", color.soft);
  map.style.setProperty("--map-text-color", color.text);
  map.style.setProperty("--map-foreground-color", color.foreground);
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
  const editing = event.target instanceof Element
    && event.target.matches("input, textarea, select, [contenteditable='true']");
  if (!presentation.hidden && !editing) {
    if (event.key === "ArrowLeft") moveSlide(-1);
    if (event.key === "ArrowRight") moveSlide(1);
    if (event.shiftKey && event.key.toLowerCase() === "n") toggleNotes();
    if (event.shiftKey && event.key.toLowerCase() === "f") toggleFullscreen();
    if (event.key === "Delete" && currentPresentationView === "overall") deleteSelectedCustomNode();
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
document.querySelector("#open-memory-map").addEventListener("click", () => {
  presentation.hidden = false;
  document.body.classList.add("presentation-open");
  setPresentationView("overall");
});
document.querySelector("#map-add-node").addEventListener("click", () => {
  const form = document.querySelector("#map-node-form");
  form.hidden = !form.hidden;
  if (!form.hidden) {
    populateMapParentOptions();
    if (selectedCustomNodeId) document.querySelector("#map-node-parent").value = selectedCustomNodeId;
    document.querySelector("#map-node-title").focus();
  }
});
document.querySelector("#map-node-cancel").addEventListener("click", () => {
  document.querySelector("#map-node-form").hidden = true;
});
document.querySelector("#map-node-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const title = document.querySelector("#map-node-title").value.trim();
  const url = document.querySelector("#map-node-url").value.trim();
  if (!title) return;
  customMapNodes.push({
    id: `custom:${Date.now()}`,
    parentId: document.querySelector("#map-node-parent").value,
    title,
    url,
  });
  saveStored(customMapNodesKey, customMapNodes);
  populateMapParentOptions();
  event.currentTarget.reset();
  event.currentTarget.hidden = true;
  document.querySelector("#map-save-status").textContent = "New node saved";
  rerenderOverallMap();
});
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
window.mermaid?.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  theme: preferredTheme === "dark" ? "dark" : "neutral",
});

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
populateMapParentOptions();

const presentMatch = location.hash.match(/^#present=(\d+)$/);
if (location.hash === "#map") {
  presentation.hidden = false;
  document.body.classList.add("presentation-open");
  setPresentationView("overall");
} else if (presentMatch) {
  openPresentation(Number(presentMatch[1]));
}
