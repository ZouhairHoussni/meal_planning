let draggedRecipeId = null;

const plannerSheet = document.querySelector("[data-planner-sheet]");
const plannerOverlay = document.querySelector("[data-planner-overlay]");
const plannerSheetTitle = document.querySelector("#planner-sheet-title");
const plannerSheetSubtitle = document.querySelector("[data-planner-sheet-subtitle]");
const plannerDateInput = document.querySelector("[data-planner-date-input]");
const plannerMealTypeInput = document.querySelector("[data-planner-meal-type-input]");
const plannerNextInput = document.querySelector("[data-planner-next-input]");
const plannerRecipeSearch = document.querySelector("[data-planner-recipe-search]");

function openPlannerSheet(trigger) {
  if (!plannerSheet || !plannerOverlay || !trigger) return;

  const mealLabel = trigger.dataset.mealLabel || "meal";
  const dateLabel = trigger.dataset.dateLabel || "this day";
  plannerSheetTitle.textContent = `Add ${mealLabel}`;
  plannerSheetSubtitle.textContent = `${dateLabel}`;
  plannerDateInput.value = trigger.dataset.date || "";
  plannerMealTypeInput.value = trigger.dataset.mealType || "";
  plannerNextInput.value = trigger.dataset.next || "";
  plannerSheet.classList.remove("hidden");
  plannerOverlay.classList.remove("hidden");
  plannerSheet.setAttribute("aria-hidden", "false");
  document.body.classList.add("planner-sheet-open");
  plannerRecipeSearch?.focus();
}

function closePlannerSheet() {
  if (!plannerSheet || !plannerOverlay) return;

  plannerSheet.classList.add("hidden");
  plannerOverlay.classList.add("hidden");
  plannerSheet.setAttribute("aria-hidden", "true");
  document.body.classList.remove("planner-sheet-open");
}

document.querySelectorAll("[data-planner-add-trigger]").forEach((trigger) => {
  trigger.addEventListener("click", () => openPlannerSheet(trigger));
});

document.querySelectorAll("[data-planner-close]").forEach((button) => {
  button.addEventListener("click", closePlannerSheet);
});

plannerOverlay?.addEventListener("click", closePlannerSheet);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closePlannerSheet();
  }
});

document.querySelector("[data-planner-add-current]")?.addEventListener("click", () => {
  const activePanel = document.querySelector("[data-planner-day-panel]:not([hidden])");
  const slots = Array.from(activePanel?.querySelectorAll(".planner-slot") || []);
  const firstEmptySlot = slots.find((slot) => slot.querySelector(".planner-empty-slot"))?.querySelector(
    "[data-planner-add-trigger]",
  );
  const firstSlot = activePanel?.querySelector("[data-planner-add-trigger]");
  openPlannerSheet(firstEmptySlot || firstSlot);
});

document.querySelectorAll("[data-planner-day-tab]").forEach((tab) => {
  tab.addEventListener("click", () => {
    const selectedDate = tab.dataset.plannerDayTab;
    document.querySelectorAll("[data-planner-day-tab]").forEach((candidate) => {
      candidate.setAttribute("aria-selected", String(candidate === tab));
    });
    document.querySelectorAll("[data-planner-day-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.plannerDayPanel !== selectedDate;
    });
  });
});

plannerRecipeSearch?.addEventListener("input", () => {
  const query = plannerRecipeSearch.value.trim().toLowerCase();
  document.querySelectorAll("[data-planner-recipe-option]").forEach((option) => {
    option.hidden = query !== "" && !option.dataset.recipeName.includes(query);
  });
});

document.querySelectorAll("[data-recipe-id]").forEach((card) => {
  card.addEventListener("dragstart", (event) => {
    draggedRecipeId = card.dataset.recipeId;
    event.dataTransfer.setData("text/plain", draggedRecipeId);
    event.dataTransfer.effectAllowed = "copy";
  });
});

document.querySelectorAll(".planner-drop").forEach((slot) => {
  slot.addEventListener("dragover", (event) => {
    event.preventDefault();
    slot.classList.add("ring-2", "ring-primary");
  });

  slot.addEventListener("dragleave", () => {
    slot.classList.remove("ring-2", "ring-primary");
  });

  slot.addEventListener("drop", (event) => {
    event.preventDefault();
    slot.classList.remove("ring-2", "ring-primary");
    const recipeId = event.dataTransfer.getData("text/plain") || draggedRecipeId;
    const form = slot.querySelector(".planner-drop-form");
    const recipeInput = form?.querySelector('input[name="recipe"]');
    if (form && recipeInput && recipeId) {
      recipeInput.value = recipeId;
      form.submit();
    }
  });
});
