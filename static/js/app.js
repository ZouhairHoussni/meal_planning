document.documentElement.classList.add("js-enabled");

const shoppingQuickAddToggle = document.querySelector("[data-shopping-quick-add-toggle]");
const shoppingQuickAddPanel = document.querySelector("[data-shopping-quick-add-panel]");
const shoppingQuickAddClose = document.querySelector("[data-shopping-quick-add-close]");

function setShoppingQuickAddOpen(isOpen) {
  if (!shoppingQuickAddToggle || !shoppingQuickAddPanel) return;

  shoppingQuickAddToggle.setAttribute("aria-expanded", String(isOpen));
  shoppingQuickAddPanel.classList.toggle("hidden", !isOpen);
  shoppingQuickAddPanel.classList.toggle("shopping-quick-add-open", isOpen);
  if (isOpen) {
    shoppingQuickAddPanel.querySelector("input, select, textarea, button")?.focus();
  }
}

shoppingQuickAddToggle?.addEventListener("click", () => {
  setShoppingQuickAddOpen(shoppingQuickAddToggle.getAttribute("aria-expanded") !== "true");
});

shoppingQuickAddClose?.addEventListener("click", () => {
  setShoppingQuickAddOpen(false);
});
