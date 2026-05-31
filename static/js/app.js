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

const shoppingPurchasedToggle = document.querySelector("[data-shopping-purchased-toggle]");
const shoppingPurchasedPanel = document.querySelector("[data-shopping-purchased-panel]");
const shoppingPurchasedLabel = document.querySelector("[data-shopping-purchased-label]");

function setShoppingPurchasedOpen(isOpen) {
  if (!shoppingPurchasedToggle || !shoppingPurchasedPanel) return;

  shoppingPurchasedToggle.setAttribute("aria-expanded", String(isOpen));
  shoppingPurchasedPanel.classList.toggle("hidden", !isOpen);
  shoppingPurchasedPanel.classList.toggle("shopping-purchased-panel-open", isOpen);
  if (shoppingPurchasedLabel) {
    shoppingPurchasedLabel.textContent = isOpen ? "Hide purchased items" : "Show purchased items";
  }
}

shoppingPurchasedToggle?.addEventListener("click", () => {
  setShoppingPurchasedOpen(shoppingPurchasedToggle.getAttribute("aria-expanded") !== "true");
});

document.querySelectorAll("[data-shopping-purchase-form]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (form.dataset.submitting === "true") return;

    event.preventDefault();
    form.dataset.submitting = "true";
    form.closest("[data-shopping-item]")?.classList.add("shopping-item-leaving");
    window.setTimeout(() => form.submit(), 240);
  });
});
