# MealBudget Decisions

Status: Phase 0 decisions recorded after implementation.

## Accepted Product Defaults

- Currency: EUR.
- Units: metric units only for MVP: g, kg, ml, l and unit.
- Week start: Monday.
- Timezone: Europe/Paris.
- UI language: English for MVP, with future i18n kept possible.
- Price source: manual estimates and actual user-entered prices only.
- Household model: single owned household per user in MVP.
- Frontend: Django server-rendered HTML, vanilla JavaScript, Tailwind CDN.
- No AI, OCR, barcode, supermarket API, scraping, PWA or SPA work during MVP.

## Proposed Technical Decisions for Phase 0

### Python and Django versions

Decision: Python 3.12 and Django 5.2.14 LTS.

Reason: Python 3.12 is available locally. Django 6.0.5 is the latest release, but Django 5.2.14 is the current LTS line and is the calmer baseline for this MVP.

### Dependency management

Decision: `requirements.txt` for the MVP.

Reason: this is a small Django monolith with a deliberately simple stack. A pinned `requirements.txt` is easy to inspect and adequate until packaging or multi-environment complexity appears.

### Database and tests

Decision: PostgreSQL for development and test runs, with `compose.yaml` providing a local `postgres:17-alpine` service.

Reason: the project relies on Decimal fields, uniqueness constraints, transactions and later query behavior. SQLite would be faster but could hide the exact behavior we care about.

### User identity

Decision: Django's built-in `User` model using username plus email field in Phase 0/1, with email-oriented UI copy where practical. Do not introduce a custom user model or allauth yet.

Reason: this avoids early authentication complexity. The user-facing registration form can still collect email. If true email-as-login becomes a hard requirement, decide before migrations become costly.

### App boundaries

Decision: start with a tiny `core` app in Phase 0; add the following domain apps only when their phase begins.

- `core`: shared views, dates, template shell, lightweight utilities.
- `accounts`: registration and onboarding routing glue.
- `households`: household profile and default budget.
- `recipes`: ingredients, recipe models and costing in Phase 2.
- `planning`: meal plans and weekly slots in Phase 3.
- `pantry`: pantry stock in Phase 4.
- `shopping`: grocery list, shopping mode and purchase truth in Phases 4-5.
- `insights`: read-only summaries in Phase 6.

Reason: these boundaries match the product loop while keeping each app understandable.

### Money

Decision: use `Decimal` in Python and `DecimalField`/PostgreSQL numeric fields in the database. Never use floats for money.

Reason: this is a budget product; rounding errors would directly damage user trust.

### Phase 0 auth shell

Decision: Phase 0 may include Django built-in login/logout pages and a protected placeholder dashboard, but not custom registration or household onboarding.

Reason: this resolves the Phase 0/Phase 1 overlap in the master spec and keeps the first implementation slice small.

### Test runner plugin isolation

Decision: `pytest.ini` disables the globally installed `pytest-flask` plugin with `-p no:flask`.

Reason: the user's Python environment has `pytest-flask` installed globally. It shadows the Django `client` fixture and breaks pytest-django tests unless disabled for this repository.

### Local debug default

Decision: `DJANGO_DEBUG` defaults to `True` when no `.env` is present.

Reason: Phase 0 is local development setup. Production-like deployment must explicitly provide environment variables and set `DJANGO_DEBUG=False`.

### Early vertical product loop

Decision: the 2026-05-25 user request moved a compact recipe -> planner -> shopping loop ahead of the original phase order.

Reason: the user wanted the sidebar entries to be real workflows immediately, with signup, recipe components, planner drag/drop, breakfast/lunch/dinner/extra slots and manual grocery additions.

Impact: household onboarding, budget modeling, ingredient catalogue/pricing and pantry deduction are still pending. The current implementation is intentionally simple and should be refined rather than treated as the final domain model.

### Breakfast and extra meal slots

Decision: planner meal types now include `breakfast`, `lunch`, `dinner` and `extra`.

Reason: this is an explicit user request and supersedes the original MVP spec that limited planning to lunch/dinner.

### Drag-and-drop planner

Decision: a small vanilla JavaScript drag/drop enhancement is implemented for recipe cards.

Reason: this is an explicit user request. The implementation still uses server-side POST forms as the durable source of truth.

### Simplified recipe components

Decision: the first recipe implementation stores component name, quantity, unit and note directly on `RecipeComponent`.

Reason: this makes recipe creation and shopping sync usable now. It is a stepping stone toward the richer ingredient catalogue and price model.

### Recipe component store hints

Decision: `RecipeComponent` can now store optional `brand` and `store` values, and planned shopping sync copies those values onto generated shopping lines.

Reason: the user wants recipe components to carry practical buying context. This is still lightweight metadata, not a normalized store catalogue or price-history model.

### Shopping sync

Decision: visiting or updating shopping syncs planned items from all planned recipe components and preserves manual shopping extras.

Reason: this gives the requested automatic shopping list behavior. It does not yet preserve purchased planned-item state across re-syncs and is not suitable for completed shopping history until Phase 5 is properly implemented.

### Shopping item price metadata

Decision: `ShoppingItem` now stores optional `price`, `brand` and `store` fields.

Reason: the user needs to attribute prices and remember where/which brand a grocery line came from. This is intentionally line-level metadata for now, not yet a full price-history model.

### Shopping summary selector

Decision: shopping totals are calculated in `shopping/selectors.py` instead of directly in templates.

Reason: price totals and missing-price counts are business-facing summaries that need tests and reuse on both Shopping and Dashboard.

### Early dashboard insights

Decision: Dashboard insight cards use existing planned meals, recipe components and shopping-line prices to show most planned meal, top components and known spend by store. Store and source filters apply to shopping spend summaries.

Reason: this gives useful feedback now without introducing a separate analytics app or premature budget-history model.

Impact: "budget by store" currently means known priced shopping-line spend by store. True weekly budget allocation, actual-vs-estimated variance and completed shopping history remain later Phase 5/6 work.

### Household onboarding slice

Decision: implement a single owned `Household` in the `households` app before pantry deduction or completed shopping history.

Reason: the budget-first product loop needs a stable owner/budget context. This also gives new users a clearer first-run path after signup.

Impact: existing authenticated users without a household will be routed to onboarding before using the dashboard. Existing owner-scoped recipe, planner, shopping and pantry data remains user-owned for now; moving those models to household scope is a later migration.

### Weekly budget status

Decision: in this slice, dashboard budget status compares the household's weekly EUR budget to the current known shopping-line spend.

Reason: the app does not yet have completed shopping trips or immutable weekly list snapshots. Showing known spend against budget is useful now and honest enough if the UI labels it clearly.

Impact: this is not yet actual weekly spend history. Phase 5/6 must replace this with list/trip snapshots once completed shopping is implemented.

### Pantry updates from shopping

Decision: marking a shopping item as purchased should synchronize that item into pantry stock. The sync must be idempotent and reversible while the shopping line remains editable.

Reason: users expect bought groceries to become available pantry stock, but repeated toggles or edits must not duplicate inventory.

Impact: shopping items will store the pantry quantity/name/unit currently applied. Updating or unchecking a purchased item can then subtract the previous pantry contribution before applying the new one.

### Grocery price strategy

Decision: price estimates should be manual-first, then remembered in a local user-owned price memory by item, unit, brand and store. External APIs are deferred until the core workflows are stable.

Reason: supermarket APIs are fragmented, country/store-specific, often incomplete, and may have usage/terms constraints. A local price memory gives useful automatic estimates quickly from the user's own shopping history without adding integration risk.

Impact: the next pricing slice should introduce a `PriceEstimate` or `PriceObservation` model populated from shopping entries. When users add a grocery item or generated planned item, the app can suggest or auto-fill the most recent matching price for that store/brand. Public/store APIs can be evaluated later as optional import sources.

### Shopping phone UX

Decision: the shopping page is designed as a phone-first checklist with large circular bought controls, sticky quick add, separated "still to buy" and "already in pantry" sections, and inline edit details.

Reason: shopping happens one-handed in a store. The primary action must be tap-to-buy, while price/brand/store edits remain available without making every item feel like a dense spreadsheet row.

Impact: shopping remains server-rendered and works without a JavaScript framework. Further polish should keep the same checklist mental model and avoid hiding the core buy/unbuy action behind menus.

### Mobile-first visual identity

Decision: the app now uses a shared blue-and-yellow design system across all user-facing server-rendered pages.

Reason: the previous MVP shell was functional but visually flat, mostly black-and-white, and inconsistent across dashboard, planner, recipes, pantry, shopping, auth and household flows. The product needs a recognizable, warm and practical identity before adding more feature depth.

Implementation: reusable tokens and component classes live in `templates/base.html` and `static/css/app.css`. The baseline palette is vibrant blue for primary actions, warm yellow for emphasis, navy for structure, cream/off-white for warm surfaces, green for positive states and orange/red for warnings. Core reusable classes cover app shell, mobile bottom nav, page heroes, cards, stats, forms, buttons, chips, empty states and shopping checklist cards.

Impact: future templates should prefer these shared classes over page-specific Tailwind clusters. The app remains Django-rendered HTML with vanilla JavaScript and Tailwind CDN; no frontend framework or build pipeline was introduced.

Update on 2026-05-27: palette tuning kept blue as the trust/action color and gold as the food warmth cue, while warming the cream surfaces and adding a fresher green for pantry/success states. This keeps the app budget-first without making it feel cold or purely financial.

### Slot-first planner interaction

Decision: the planner page should make meal slots the primary interaction target, especially on mobile. Users tap `+ Add breakfast`, `+ Add lunch`, `+ Add dinner` or `+ Add extra` inside the desired day slot, then choose a recipe from a shared add-meal panel.

Reason: mobile users should not have to select date and meal type in a separate form after already deciding where the meal belongs. Destination-first planning reduces cognitive load and keeps thumb actions close to the relevant slot.

Impact: the existing `planner_add` POST route remains authoritative and unchanged in shape. The UI pre-fills hidden date and meal type fields from the tapped slot. Drag-and-drop remains a desktop enhancement, but no longer drives the primary mobile workflow.

## Proposed Decisions for Later Phases

### Ingredient estimates

Proposed: store user-entered estimate basis as `price_amount`, `price_quantity` and `price_unit`; compute canonical-unit prices in services when needed rather than storing awkward "price per gram" values as the primary user-facing truth.

Reason: users think in "2.20 EUR per kg" or "2.80 EUR per 6 units"; the app can normalize internally without making the UI strange.

### Unit conversion

Proposed: implement a tiny domain module for unit dimensions and conversion before recipe costing.

Reason: this logic is central and easy to test. It should not live in forms, templates or JavaScript.

### Shopping history

Proposed: use `GroceryList` plus snapshot `GroceryListItem` lines for MVP, and make completed lists immutable except explicit adjustment actions. Do not introduce separate `ShoppingTrip` and `PurchaseItem` models unless Phase 5 shows a clear need.

Reason: snapshot list items are simpler and still preserve historical actual spend if regeneration is blocked after shopping starts/completion.

### Pantry consumption

Decision: grocery generation records pantry coverage as a snapshot only. Planning and list generation do not consume pantry stock.

Reason: this avoids surprising inventory changes and matches the master spec.

Update on 2026-05-31: an explicit user request moves confirmed meal consumption into the active slice. Planning still does not consume pantry stock. A planned meal may deduct stock only after the user marks it as cooked. The application records the quantities actually deducted so the action can be undone exactly. Skipped and postponed outcomes do not deduct stock. Manual pantry quantity adjustment remains available for real-world corrections.

### Purchased shopping-line preservation

Decision: purchased shopping lines are recoverable purchase history and must not be silently deleted or rewritten when planned meals change.

Reason: shopping records describe groceries that entered the home. Planner refresh may create a new pending line for a continuing need, but it must preserve already purchased lines so pantry sync and undo remain trustworthy.

Impact: the current compact shopping model still does not replace the future immutable grocery-list snapshot design, but it now protects completed line-level purchase truth.

### Dynamic recipe ingredient rows

Proposed: start with Django formsets and progressive vanilla JavaScript cloning. Keep a full-page non-modal fallback.

Reason: formsets keep server validation authoritative and avoid a fragile custom client-side state machine.

### i18n readiness

Proposed: keep copy centralized in templates and avoid hard-coded currency symbols in calculations, but do not add full translation machinery in Phase 0.

Reason: MVP language is English. Premature i18n can slow the first vertical slices, but the code should not make later French translation painful.

## Open Questions Before Phase 0

- Confirm whether username-based login remains acceptable for MVP before Phase 1 registration is implemented.
