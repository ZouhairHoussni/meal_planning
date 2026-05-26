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

### Dynamic recipe ingredient rows

Proposed: start with Django formsets and progressive vanilla JavaScript cloning. Keep a full-page non-modal fallback.

Reason: formsets keep server validation authoritative and avoid a fragile custom client-side state machine.

### i18n readiness

Proposed: keep copy centralized in templates and avoid hard-coded currency symbols in calculations, but do not add full translation machinery in Phase 0.

Reason: MVP language is English. Premature i18n can slow the first vertical slices, but the code should not make later French translation painful.

## Open Questions Before Phase 0

- Confirm whether username-based login remains acceptable for MVP before Phase 1 registration is implemented.
