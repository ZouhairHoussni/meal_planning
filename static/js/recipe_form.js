const addComponentButtons = document.querySelectorAll("#add-component, #add-component-mobile");
const componentFormset = document.querySelector("#component-formset");
const emptyComponentTemplate = document.querySelector("#component-empty-form");
const totalFormsInput = document.querySelector("#id_components-TOTAL_FORMS");

function componentRows() {
  return Array.from(document.querySelectorAll('[data-component-row="live"]'));
}

function componentField(row, suffix) {
  return row.querySelector(`[name$="-${suffix}"]`);
}

function updateComponentSummary(row) {
  const name = componentField(row, "name")?.value.trim();
  const quantity = componentField(row, "quantity")?.value.trim();
  const unit = componentField(row, "unit")?.value;
  const brand = componentField(row, "brand")?.value.trim();
  const store = componentField(row, "store")?.value.trim();
  const title = row.querySelector("[data-component-summary-title]");
  const meta = row.querySelector("[data-component-summary-meta]");

  if (title) {
    title.textContent = name || "New component";
  }

  const details = [];
  if (quantity) details.push(`${quantity} ${unit || ""}`.trim());
  if (brand) details.push(brand);
  if (store) details.push(store);
  if (meta) {
    meta.textContent = details.length ? details.join(" - ") : "Tap to edit details";
  }
}

function setComponentCollapsed(row, collapsed) {
  const summary = row.querySelector("[data-component-summary]");
  row.classList.toggle("component-row-collapsed", collapsed);
  summary?.setAttribute("aria-expanded", String(!collapsed));
  updateComponentSummary(row);
}

function openComponentRow(row) {
  componentRows().forEach((candidate) => {
    setComponentCollapsed(candidate, candidate !== row);
  });
  componentField(row, "name")?.focus();
}

function wireComponentRow(row) {
  if (row.dataset.componentWired === "true") return;
  row.dataset.componentWired = "true";

  row.querySelector("[data-component-summary]")?.addEventListener("click", () => {
    const isCollapsed = row.classList.contains("component-row-collapsed");
    if (isCollapsed) {
      openComponentRow(row);
    } else {
      setComponentCollapsed(row, true);
    }
  });

  row.querySelectorAll("input, select").forEach((field) => {
    field.addEventListener("input", () => updateComponentSummary(row));
    field.addEventListener("change", () => updateComponentSummary(row));
  });

  updateComponentSummary(row);
}

function initializeComponentAccordion() {
  componentRows().forEach((row, index) => {
    wireComponentRow(row);
    setComponentCollapsed(row, index > 0);
  });
}

if (addComponentButtons.length && componentFormset && emptyComponentTemplate && totalFormsInput) {
  initializeComponentAccordion();

  addComponentButtons.forEach((button) =>
    button.addEventListener("click", () => {
      const index = Number.parseInt(totalFormsInput.value, 10);
      const markup = emptyComponentTemplate.innerHTML.replaceAll("__prefix__", index);
      componentFormset.insertAdjacentHTML("beforeend", markup);
      totalFormsInput.value = index + 1;

      const insertedRows = Array.from(componentFormset.querySelectorAll("[data-component-row]"));
      const newRow = insertedRows.at(-1);
      if (newRow) {
        newRow.setAttribute("data-component-row", "live");
        wireComponentRow(newRow);
        openComponentRow(newRow);
        newRow.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }),
  );
}
