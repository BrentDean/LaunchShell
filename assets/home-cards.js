async function loadHomeCards() {
  const targets = document.querySelectorAll("[data-card-section]");

  if (!targets.length) {
    return;
  }

  try {
    const response = await fetch("data/site-index.json");

    if (!response.ok) {
      throw new Error(`Could not load site index: ${response.status}`);
    }

    const items = await response.json();

    targets.forEach((target) => {
      const sectionName = target.dataset.cardSection;
      const cards = items.filter((item) => item.homeSection === sectionName);

      target.innerHTML = cards.map(renderCard).join("");
    });
  } catch (error) {
    console.error(error);
  }
}

function renderCard(item) {
  const tagClass = item.type === "Guide" || item.type === "Resource" ? "tag green" : "tag";
  const buttonText = getButtonText(item);

  return `
    <article class="card linked-card">
      <a class="card-link" href="${item.url}" aria-label="Open ${escapeHtml(item.title)}"></a>
      <img src="${item.image}" alt="${escapeHtml(item.title)} card graphic" />
      <div class="card-body">
        <span class="${tagClass}">${escapeHtml(item.type)}</span>
        <h3>${escapeHtml(item.title)}</h3>

        <div class="card-meta">
          <span>${escapeHtml(item.level)}</span>
          <span>${escapeHtml(item.time)}</span>
          <span>${escapeHtml(item.category)}</span>
        </div>

        <p>${escapeHtml(item.summary)}</p>
        <a class="button" href="${item.url}">${buttonText}</a>
      </div>
    </article>
  `;
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

loadHomeCards();
