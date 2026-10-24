document.addEventListener("DOMContentLoaded", () => {
  const cards = [...document.querySelectorAll(".card")];
  const chips = document.querySelectorAll(".chip");
  const search = document.getElementById("search");
  const noResults = document.getElementById("no-results");
  const modal = document.getElementById("modal");
  const player = document.getElementById("player");
  const modalTitle = document.getElementById("modal-title");

  let activeFilter = "all";

  // Filter by category chip + search text
  function applyFilters() {
    const q = (search?.value || "").trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matchCat = activeFilter === "all" || card.dataset.category === activeFilter;
      const matchText = !q || card.dataset.title.includes(q);
      const show = matchCat && matchText;
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    if (noResults) noResults.hidden = visible !== 0 || cards.length === 0;
  }

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      activeFilter = chip.dataset.filter;
      applyFilters();
    });
  });

  search?.addEventListener("input", applyFilters);

  // Video modal
  function openVideo(card) {
    player.src = card.dataset.src;
    modalTitle.textContent = card.dataset.name;
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    player.play().catch(() => {});
  }

  function closeVideo() {
    player.pause();
    player.removeAttribute("src");
    player.load();
    modal.hidden = true;
    document.body.style.overflow = "";
  }

  cards.forEach(card => {
    card.addEventListener("click", () => openVideo(card));
    card.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openVideo(card); }
    });
  });

  modal?.querySelectorAll("[data-close]").forEach(el => el.addEventListener("click", closeVideo));
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !modal.hidden) closeVideo();
  });
});
