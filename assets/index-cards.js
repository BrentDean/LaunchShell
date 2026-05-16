async function loadIndexCards() {
  const script = document.currentScript;
  const jsonUrl = script?.dataset.json || "../data/site-index.json";
  const basePath = script?.dataset.basePath || "../";

  const targets = document.querySelectorAll("[data-index-type]");

  if (!targets.length) {
    return;
  }

  try {
    const response = await fetch(jsonUrl);

    if (!response.ok) {
      throw new Error(`Could not load site index: ${response.status}`);
    }

    const items = await response.json();

    targets.forEach((target) => {
      const allowedTypes = target.dataset.indexType
        .split(",")
        .map((type) => type.trim())
        .filter(Boolean);

      const excludedUrls = (target.dataset.excludeUrl || "")
        .split(",")
        .map((url) => url.trim())
        .filter(Boolean);

      const cards = items.filter((item) => {
        return allowedTypes.includes(item.type) && !excludedUrls.includes(item.url);
      });

      target.innerHTML = cards.map((item) => renderIndexCard(item, basePath)).join("");
    });
  } catch (error) {
    console.error(error);

    targets.forEach((target) => {
      target.innerHTML = `
        <div class="empty-state">
          Card index could not load. Check <code>data/site-index.json</code> and the local server.
        </div>
      `;
    });
  }
}

function renderIndexCard(item, basePath) {
  const tagClass = item.type === "Guide" || item.type === "Resource" ? "tag green" : "tag";
  const url = makeRelative(item.url, basePath);
  const image = makeRelative(item.image, basePath);
  const buttonText = getButtonText(item);

  return `
    <article class="card linked-card">
      <a class="card-link" href="${url}" aria-label="Open ${escapeHtml(item.title)}"></a>
      <img src="${image}" alt="${escapeHtml(item.title)} card graphic" />
      <div class="card-body">
        <span class="${tagClass}">${escapeHtml(item.type)}</span>
        <h3>${escapeHtml(item.title)}</h3>

        <div class="card-meta">
          <span>${escapeHtml(item.level)}</span>
          <span>${escapeHtml(item.time)}</span>
          <span>${escapeHtml(item.category)}</span>
        </div>

        <p>${escapeHtml(item.summary)}</p>
        <a class="button" href="${url}">${buttonText}</a>
      </div>
    </article>
  `;
}

function makeRelative(path, basePath) {
  if (
    path.startsWith("http://") ||
    path.startsWith("https://") ||
    path.startsWith("#") ||
    path.startsWith("/")
  ) {
    return path;
  }

  return `${basePath}${path}`;
}

function getButtonText(item) {
  if (item.type === "Guide") {
    return "Read the guide";
  }

  if (item.type === "Project") {
    return "Open the project";
  }

  if (item.type === "Resource") {
    return "Open resource";
  }

  return "Open";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadIndexCards();
