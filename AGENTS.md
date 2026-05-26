# AGENTS.md - MealBudget Repository Instructions for Codex

## Project mission

Build MealBudget, a modern budget-first weekly meal planning and grocery tracking web application for euro/metric households. The authoritative product and UX specification is `MEALBUDGET_CODEX_MASTER_SPEC.md`; read it before planning or implementing features.

## Working approach

- For substantial work, analyse the repository and produce/update `docs/IMPLEMENTATION_PLAN.md` before editing implementation files.
- Maintain `docs/DECISIONS.md` for architectural, data-model and UX decisions.
- Implement one coherent vertical slice at a time.
- Follow TDD: write/update a failing test for new behaviour, implement minimally, refactor, run tests, report results.
- Do not claim completion without listing verification commands and results.

## Required stack and constraints

- Django server-rendered web application.
- PostgreSQL database.
- HTML/CSS and vanilla JavaScript.
- Tailwind CSS through CDN for MVP; do not introduce a Node/Tailwind build pipeline unless explicitly requested later.
- Use `Decimal`/database decimal fields for money; never floats.
- Use EUR, metric units, Monday week start and Europe/Paris assumptions for MVP.
- No React, Vue, SPA rewrite, AI features, receipt OCR, barcode or supermarket integrations during MVP unless explicitly requested.

## Architecture rules

- Keep views thin; keep important calculations/workflows in testable service modules.
- Validate data through forms/models/services; server is authoritative.
- Scope all household data access to the authenticated user's household.
- Preserve completed shopping history; do not silently rewrite actual spend when a meal plan changes.
- Record material departures from the master spec in `docs/DECISIONS.md`.

## UX/UI rules

- Design must feel modern, calm, warm and practical, with excellent mobile shopping usability.
- Maintain consistent design tokens, spacing, cards, buttons, statuses and form styles.
- Budget state must remain visible in planner/shopping flows.
- Include empty, validation and over-budget states on implemented user-facing pages.
- Accessibility is part of done: labels, focus states, keyboard accessibility, readable contrast, touch-friendly shopping controls.

## Definition of done

Before reporting a task complete:

1. Run relevant tests and report exact command/results.
2. Ensure migrations are present when models change.
3. Check household authorisation when new data pages/actions are added.
4. Check responsive rendering conceptually and provide manual visual verification steps for UI work.
5. Update docs when setup or important decisions change.
6. Summarise changed files, remaining limitations and the recommended next slice.
