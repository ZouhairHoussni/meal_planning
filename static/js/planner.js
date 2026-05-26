let draggedRecipeId = null;

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
