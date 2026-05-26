# MealBudget Implementation Plan

Status: Phase 0 implemented, plus an early compact recipe/planner/shopping slice requested by the user on 2026-05-25. Phase 1 household onboarding and weekly budget foundation implemented on 2026-05-26.

## Source Documents

- `MEALBUDGET_CODEX_MASTER_SPEC.md` is the product, UX and engineering source of truth.
- `AGENTS.md` contains persistent repository instructions and is now present at the repository root.

## Critical Review

The product direction is coherent: the strongest loop is weekly budget -> meal plan -> pantry-aware shopping list -> actual spend -> next-week feedback. That should remain the spine of every phase.

Important issues to resolve or constrain:

- The master spec says planning should create `AGENTS.md`, but the first task asks for planning docs only and to stop before features. Defer root `AGENTS.md` creation to Phase 0 unless explicitly approved sooner.
- Phase 0 currently includes auth shell and a login-protected dashboard, while Phase 1 includes registration/login/logout. To avoid a half-authenticated product, Phase 0 should use Django's built-in auth URLs/templates only as shell plumbing, and Phase 1 should deliver the real registration/onboarding flow.
- PostgreSQL is required, but the spec does not say whether tests may use SQLite. Use PostgreSQL for development and test runs so constraints, decimal behavior and transactions match production. Avoid SQLite except for emergency local diagnosis.
- "Use sample recipes" conflicts slightly with strict user-data expectations. Treat sample recipes as explicit user-imported demo templates, not hidden production data.
- Pantry deduction is a generated-list snapshot, not real inventory consumption. This is correct for MVP but must be made very explicit in UI copy so users do not think pantry stock was decremented.
- Completed shopping history must not be rewritten. This pushes the shopping design toward immutable completed grocery list snapshots rather than live recipe-derived lines after completion.
- Recipe costing and grocery generation depend on unit compatibility. Unit conversion should be built as a small tested domain module before recipe UI complexity.
- The app list in the spec is broad. The MVP should avoid implementing Insights as a separate deep feature until actual shopping data exists. Before then, keep an empty/placeholder page or omit nav depth until useful.
- Tailwind CDN is fine for MVP speed, but any custom design tokens should live in a small base stylesheet and/or CDN config in `base.html`, not scattered across templates.
- The spec asks for modern UX and server-rendered Django. Do not introduce modals, dynamic formsets or bottom sheets until the full-page form path is solid and tested.
- User request on 2026-05-25 explicitly moved signup, clickable Planner/Shopping/Recipes/Pantry pages, recipe components, drag-and-drop planning, breakfast slots, extra meals and manual shopping additions into the current slice. This intentionally jumps ahead of the original strict phase order.

## Phased Plan

### Phase 0: Repository Foundation and Design Shell

Status: complete for the approved foundation slice.

Goal: create a running Django/PostgreSQL project with tests, configuration, docs and a modern authenticated shell. No domain features beyond a protected placeholder dashboard.

TDD focus:

- Configuration smoke tests.
- Authenticated dashboard access behavior.
- Template shell rendering enough structure to support later UI work.

Deliverables:

- Django project and base apps.
- PostgreSQL environment configuration via environment variables.
- Test harness using `pytest` and `pytest-django`.
- Tailwind CDN in the base template with stable design token conventions.
- Static CSS/JS directories.
- Built-in login/logout pages styled through the auth shell.
- Login-protected placeholder dashboard.
- README setup instructions, `.env.example`, root `AGENTS.md`, and maintained docs.

Definition of done:

- `python manage.py check` passes.
- `pytest` passes.
- Local server boots with documented commands.
- `/dashboard/` redirects anonymous users and renders for authenticated users.

### Phase 1: Household Onboarding and Weekly Budget

Goal: a new user can register, create a household, set a EUR weekly budget, and land in a personalized current-week empty dashboard/planner context.

TDD focus:

- Registration creates a user without creating duplicate household state.
- Onboarding creates exactly one owned household.
- Budget validation uses `Decimal`, requires positive values, and stores EUR.
- Current week helper always returns Monday for Europe/Paris date context.
- Private pages require login and scope by the authenticated user's household.

Deliverables:

- Registration view/form.
- Household model and initial migration.
- Onboarding form/view.
- Household ownership helpers/middleware or request helper.
- Current-week helper.
- Dashboard empty state with "Plan this week" CTA.
- Basic household settings route if needed for budget edits.

Definition of done:

- Registration -> onboarding -> dashboard/planner route works.
- A user owns exactly one MVP household.
- Budget and servings validation are covered by tests.
- Empty dashboard reflects household budget and selected week.

Status:

- Signup is implemented with Django's built-in `User` model.
- Add a single owned `Household` per user.
- Redirect signup to onboarding.
- Redirect authenticated users without a household from dashboard to onboarding.
- Store EUR weekly budget and default servings.
- Show budget-aware dashboard totals using the existing shopping summary.
- Add a small household settings page for editing budget and household defaults.

Out of scope for this slice:

- Multiple households.
- Invitations or shared household membership.
- Completed shopping history.
- Pantry deduction.
- Ingredient price catalogue.
- True weekly shopping-list snapshots.

### Phase 2: Ingredients and Recipe Library

Goal: users can maintain ingredients and create cost-aware recipes.

Key build order:

- Unit conversion module and tests.
- Ingredient model/forms with case-insensitive household uniqueness.
- Recipe and recipe ingredient models/forms.
- Recipe costing service.
- Recipe library/detail/create/edit pages.

Partial status:

- A simplified recipe library, recipe detail and recipe create form are implemented.
- Recipe edit is implemented.
- Recipe components are simple grocery-style rows stored directly on `RecipeComponent` with optional brand and store hints; full ingredient catalogue/pricing is still pending.

### Phase 3: Weekly Planner

Goal: users can fill lunch/dinner slots and see estimated weekly meal cost against the budget.

Key build order:

- MealPlan and PlannedMeal models with week/date constraints.
- Planner selector and empty states.
- Add/edit/remove slot flows using standard Django POST/Redirect/GET.
- Weekly estimate service.
- Mobile-friendly selected-day layout.

Partial status:

- A simplified weekly planner is implemented with breakfast, lunch, dinner and extra slots.
- Recipe cards can be dragged into slots with vanilla JavaScript, backed by normal POST forms.
- Weekly budget calculations and household week settings are still pending.

### Phase 4: Pantry-Aware Grocery Generation

Goal: planned meals become an accurate draft shopping list.

Key build order:

- Pantry model/forms.
- Pantry coverage service.
- GroceryList/GroceryListItem models.
- Generation service with snapshots.
- Draft list review UI grouped by category.

Partial status:

- A basic pantry page exists and is clickable.
- Pantry updates from purchased shopping items are the next active slice.
- Planned recipe components sync into shopping items.

### Phase 5: Mobile Shopping Mode and Actual Spend

Goal: the shopping flow records reality without corrupting historical plans.

Key build order:

- Start/complete shopping lifecycle.
- Touch-friendly checklist.
- Actual price entry and skipped/unavailable states.
- Manual extras.
- Completed list immutability tests.

Partial status:

- A basic shopping list exists with planned items and manual extras.
- Purchased/unpurchased toggles exist.
- Shopping items can store optional price, brand and store.
- Shopping and dashboard now show known spend totals, priced item counts and missing-price counts.
- Actual prices, completed trips and immutable history are still pending.

### Phase 6: Dashboard and Insight Refinement

Goal: close the feedback loop with useful weekly summaries.

Key build order:

- Actual vs estimated dashboard cards.
- Planned vs extra spending breakdown.
- Price variance explanation.
- Costliest recipes when data is complete.
- Empty and missing-price states.

Partial status:

- The dashboard now previews the most planned meal, top planned components and known spend by store.
- Dashboard filters support store and source for shopping spend summaries.
- These insights are based on current planning and shopping-line data only; true budget variance and completed shopping history remain pending.

## Phase 0 Exact Files

Create:

- `AGENTS.md`
- `MEALBUDGET_CODEX_MASTER_SPEC.md`
- `README.md`
- `.gitignore`
- `.env.example`
- `compose.yaml`
- `requirements.txt`
- `pytest.ini`
- `manage.py`
- `config/__init__.py`
- `config/settings.py`
- `config/urls.py`
- `config/asgi.py`
- `config/wsgi.py`
- `core/__init__.py`
- `core/apps.py`
- `core/views.py`
- `core/urls.py`
- `core/tests/test_dashboard_access.py`
- `templates/base.html`
- `templates/layouts/app_shell.html`
- `templates/layouts/auth_shell.html`
- `templates/registration/login.html`
- `templates/registration/logged_out.html`
- `templates/core/dashboard.html`
- `templates/components/budget_progress.html`
- `templates/components/empty_state.html`
- `templates/components/mobile_bottom_nav.html`
- `static/css/app.css`
- `static/js/app.js`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/DECISIONS.md`

Do not create Phase 1 domain models in Phase 0.

## Phase 0 Dependencies

Pin exact versions during implementation:

- Python: prefer 3.12 unless the local runtime requires 3.11.
- Django: current stable LTS/non-LTS selected at implementation time and recorded.
- `psycopg[binary]` for PostgreSQL.
- `django-environ` or `python-decouple` for environment settings. Prefer `django-environ`.
- `pytest`.
- `pytest-django`.
- Optional but recommended in Phase 0: `ruff` for fast linting. Do not block MVP on a complex formatting stack.

## Phase 0 Tests

Create:

- `core/tests/test_dashboard_access.py`
  - anonymous user is redirected from `/dashboard/`;
  - authenticated user receives HTTP 200 from `/dashboard/`;
  - dashboard uses the app shell and contains the placeholder empty state.
- Optional config smoke test:
  - URL names for dashboard and auth routes resolve.

## Phase 1 Exact Files

Create/update:

- `accounts/__init__.py`
- `accounts/apps.py`
- `accounts/forms.py`
- `accounts/views.py`
- `accounts/urls.py`
- `accounts/tests/test_registration.py`
- `households/__init__.py`
- `households/apps.py`
- `households/models.py`
- `households/forms.py`
- `households/selectors.py`
- `households/services.py`
- `households/urls.py`
- `households/views.py`
- `households/migrations/0001_initial.py`
- `households/tests/test_household_model.py`
- `households/tests/test_onboarding.py`
- `core/dates.py`
- `core/tests/test_dates.py`
- `core/views.py`
- `templates/accounts/register.html`
- `templates/households/onboarding.html`
- `templates/households/settings.html`
- `templates/core/dashboard.html`
- `config/settings.py`
- `config/urls.py`

## Phase 1 Dependencies

No new dependency is required beyond Phase 0. Use Django auth and forms. Do not add allauth or a custom user model unless approved before Phase 0 starts.

## Phase 1 Models

Create `Household`:

- `owner`: `ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="owned_households")`
- `name`: `CharField(max_length=120)`
- `default_servings`: `PositiveSmallIntegerField(default=2)`
- `adults_count`: `PositiveSmallIntegerField(default=0)`
- `children_count`: `PositiveSmallIntegerField(default=0)`
- `default_weekly_budget`: `DecimalField(max_digits=8, decimal_places=2)`
- `currency`: `CharField(max_length=3, default="EUR")`
- `created_at`: `DateTimeField(auto_now_add=True)`
- `updated_at`: `DateTimeField(auto_now=True)`

Constraints:

- one household per owner for MVP;
- default servings greater than zero;
- default weekly budget greater than zero;
- currency fixed to `EUR` in forms/services for MVP.

## Phase 1 Tests

Create:

- `accounts/tests/test_registration.py`
  - registration page renders;
  - valid registration creates a user and redirects to onboarding;
  - authenticated user with no household is sent to onboarding where appropriate.
- `households/tests/test_household_model.py`
  - household requires positive budget;
  - household requires positive default servings;
  - one owner cannot create two MVP households;
  - currency defaults to `EUR`.
- `households/tests/test_onboarding.py`
  - onboarding requires login;
  - valid onboarding creates a household owned by the user;
  - invalid budget redisplays validation errors without creating a household;
  - completed onboarding redirects to dashboard or current planner.
- `core/tests/test_dates.py`
  - current week helper returns Monday week start;
  - explicit dates in a week map to the same Monday;
  - timezone assumption is Europe/Paris.
- Update `core/tests/test_dashboard_access.py`
  - authenticated user without household sees onboarding redirect or setup CTA;
  - authenticated user with household sees budget-aware empty dashboard.

## Approval Gate

Stop here. Phase 0 should begin only after plan approval.
