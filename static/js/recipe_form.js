const addComponentButton = document.querySelector("#add-component");
const componentFormset = document.querySelector("#component-formset");
const emptyComponentTemplate = document.querySelector("#component-empty-form");
const totalFormsInput = document.querySelector("#id_components-TOTAL_FORMS");

if (addComponentButton && componentFormset && emptyComponentTemplate && totalFormsInput) {
  addComponentButton.addEventListener("click", () => {
    const index = Number.parseInt(totalFormsInput.value, 10);
    const markup = emptyComponentTemplate.innerHTML.replaceAll("__prefix__", index);
    componentFormset.insertAdjacentHTML("beforeend", markup);
    totalFormsInput.value = index + 1;
  });
}
