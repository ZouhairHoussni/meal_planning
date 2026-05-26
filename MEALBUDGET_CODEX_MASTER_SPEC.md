# MealBudget — Codex Master Product & Engineering Specification

> **Purpose of this document**  
> This is the authoritative product, UX/UI, architecture and implementation specification for a new Django application. Codex must read this document before proposing or writing implementation code. If a future user instruction conflicts with this document, the newer explicit user instruction wins, but Codex must mention the conflict and update documentation where necessary.

---

## 0. Instructions for Codex: how to work on this project

### 0.1 Operating mode

This is a multi-stage product build, not a one-shot code generation request.

Before implementation, Codex must:

1. Inspect the repository and determine whether it is empty, partially initialised, or already contains relevant work.
2. Read this full specification and any root `AGENTS.md` file.
3. Create or update:
   - `AGENTS.md` with persistent project working rules;
   - `docs/IMPLEMENTATION_PLAN.md` with phases, milestones and status checkboxes;
   - `docs/DECISIONS.md` with important architectural or UX decisions.
4. Propose the implementation order for the next vertical slice.
5. Ask only questions that genuinely block implementation. When a reasonable default is specified here, adopt it and record it in `docs/DECISIONS.md` instead of repeatedly asking.

### 0.2 Required development style

Use **TDD as the normal implementation method**:

1. Write or update tests that describe the next behaviour.
2. Run the tests and confirm the new tests fail for the expected reason.
3. Implement the smallest clean solution that makes them pass.
4. Refactor while keeping tests green.
5. Run the relevant test suite and report commands/results.

Do not claim TDD was followed unless a failing test was created or identified before the implementation change.

### 0.3 Delivery discipline

Work in small vertical slices that produce visible usable value. Prefer a small completed workflow over partially built models for many future features.

For each implementation task, report:

- what was implemented;
- files created or changed;
- tests added and commands run;
- screenshots/manual verification steps when UI changes are involved;
- remaining limitations and the next recommended slice.

### 0.4 Avoid these agent mistakes

Do **not**:

- implement the entire roadmap in a single uncontrolled pass;
- add external APIs, AI, receipt OCR, barcode scanning or supermarket integrations during MVP unless explicitly requested later;
- replace Django server-rendered templates with React/Vue or a frontend build pipeline;
- introduce Tailwind build tooling: this project intentionally starts with **Tailwind CSS CDN**;
- use floating-point arithmetic for money;
- embed calculation-heavy business logic in templates or views;
- hard-code grocery calculations in JavaScript only;
- add packages without explaining why they are necessary;
- create visually impressive but unusable dashboards containing invented data.

### 0.5 Product assumption to use unless changed by the user

This first version is for a household in France/Europe that wants to control food spending while planning meals. Use:

- currency: EUR (`€`);
- decimal comma in displayed money where practical through localisation, e.g. `72,40 €`;
- metric units: gram, kilogram, millilitre, litre, unit;
- week start: Monday;
- timezone: Europe/Paris;
- UI language for MVP: English copy, with structure ready for future French translation;
- prices: manually maintained estimates and actual purchase prices, not live supermarket prices.

---

# 1. Product definition

## 1.1 Working name

**MealBudget**  
A budget-first weekly meal planning and grocery tracking application.

The name can later be changed without changing domain terminology. Use `mealbudget` for the Django project package unless a repository already establishes another name.

## 1.2 One-sentence promise

MealBudget helps a household plan meals for the week, automatically calculate what groceries are missing, keep shopping within budget, and learn where food money is actually going.

## 1.3 Product thesis

Most meal planners begin with attractive recipes. Most budgeting apps treat groceries as one expense category. MealBudget connects the decisions that happen *before* spending with the spending that happens *after* shopping:

```text
Weekly budget → Meal plan → Ingredient needs → Pantry deduction → Shopping list → Actual purchases → Insight for next week
```

The application must feel like a calm weekly assistant rather than an accounting tool or recipe social network.

## 1.4 Core outcomes for the user

A successful MVP lets the user answer these questions in seconds:

1. What are we eating this week?
2. What do we need to buy?
3. What do we already have at home?
4. Will the planned week fit our food budget?
5. After shopping, did we overspend and why?

## 1.5 First target user

A budget-conscious household of one to four people, planning meals weekly and shopping in euros. They may shop at one or several supermarkets or local markets. They want convenience and control without complex finance terminology.

## 1.6 MVP differentiator

The product is **budget-first and pantry-aware**:

- Meals have estimated cost per serving.
- A weekly plan immediately shows predicted cost against the budget.
- Ingredients already in the pantry reduce the generated shopping list.
- After shopping, actual cost is recorded and compared to the estimate.
- Unplanned groceries are visible rather than hidden in totals.

---

# 2. Scope: MVP, later versions and non-goals

## 2.1 MVP scope: complete usable workflow

The MVP is complete only when a user can perform this end-to-end journey:

1. Create an account and household profile.
2. Set a weekly grocery budget.
3. Maintain an ingredient catalogue and create recipes.
4. Plan lunch and/or dinner meals for a selected week.
5. Generate a grocery list from the plan with correct portion scaling and pantry deduction.
6. Enter estimated prices where needed and see projected spend versus budget.
7. Shop using a convenient checklist and record actual prices/items.
8. View a dashboard comparing planned and actual food spend.

## 2.2 MVP features

### Authentication and household

- Register, sign in, sign out.
- One household owned by the authenticated user in MVP.
- Household name.
- Default number of servings/adults; optional child count stored for context only at first.
- Default weekly grocery budget in EUR.

### Ingredient catalogue

- Ingredient name, category, canonical base unit and optional default estimated unit price.
- Categories: vegetables, fruit, meat/fish, dairy/eggs, grains/pasta, pantry, frozen, bakery, drinks, snacks, other.
- Ingredient names are generic, such as chicken breast, onions, rice, milk.
- Prevent accidental duplicates case-insensitively per household where possible.

### Recipes

- Create, view, edit and archive recipes.
- Recipe fields: name, short description, default servings, preparation time, optional cooking time, instructions, tags.
- Recipe ingredient rows: ingredient, quantity, unit, optional note.
- Calculated estimated total cost and cost per serving.
- Tags in MVP: quick, budget-friendly, vegetarian, family-friendly, batch-cook, freezer-friendly.

### Weekly planning

- Week selector with Monday as start of week.
- Lunch and dinner slots for each day; breakfast is out of MVP scope unless later requested.
- Add a recipe to a slot and set servings for that occurrence.
- Optional free-text note per planned meal, e.g. “eat out” or “leftovers”; notes do not generate ingredients.
- Display estimated cost of planned recipes and budget status.

### Pantry

- Create and update pantry item quantities for ingredients.
- Store quantity, base unit and optional best-before date.
- MVP subtraction uses only compatible same-dimension units after normalisation.
- Mark an item as unavailable/remove it.

### Grocery list and shopping

- Generate or refresh a grocery list from a weekly plan.
- Aggregate ingredient needs across meals.
- Deduct pantry quantities from required quantities without allowing negative shopping quantities.
- Organise list by ingredient category.
- Manual additions for unplanned groceries.
- Checklist interaction suitable for a phone while shopping.
- Record actual quantity bought and actual line cost.
- Track whether an item was planned, pantry-covered, manually added, skipped or purchased.
- Select/store a shop name optionally when completing a shopping trip.

### Budget dashboard

- Current/selected week budget card.
- Estimated meal-plan spend.
- Actual recorded grocery spend.
- Remaining budget or overspend amount.
- Planned versus unplanned spending.
- Costliest recipes in the selected week when data permits.
- Clear empty states when actual purchase data does not yet exist.

## 2.3 Later capabilities: design for them, do not implement in MVP

- Shared household access and invitations.
- Leftover portions assigned to later meal slots.
- Expiry alerts and food-waste insights.
- Store-by-store price history and comparison.
- Monthly trends and exports.
- Barcode/product support through Open Food Facts.
- Receipt image parsing/OCR.
- Smart suggestions: meals from pantry, low-cost alternatives, budget optimisation.
- Nutrition/allergen analysis.
- PWA/offline shopping mode.
- French translation/i18n and additional currencies.

## 2.4 Explicit MVP non-goals

- Food delivery or online grocery ordering.
- Scraping supermarket websites.
- Automatic live price feeds.
- AI-generated recipes or medical/nutritional advice.
- Public recipe marketplace.
- Payment processing.
- Social following/reviews.

---

# 3. UX strategy and experience principles

## 3.1 Experience objective

The interface should make weekly planning feel lighter and less mentally demanding. It should not ask the user to manage database concepts such as “purchase item” or “planned meal”; it should speak in domestic actions:

- Plan week
- Add meal
- Use what I have
- Build shopping list
- Start shopping
- Finish trip
- Review spending

## 3.2 UX principles

### Principle A — Budget always stays visible

The budget is not hidden inside analytics. While planning and shopping, show a compact budget indicator:

```text
Estimated: 61,80 € of 80,00 €  ·  18,20 € left
```

Use an amber warning near the limit and a red warning above budget, but do not use alarming language.

### Principle B — The next action should be obvious

On every major page, one primary action should dominate:

- Empty dashboard: **Plan this week**
- Planner with meals: **Generate shopping list**
- Grocery list before shopping: **Start shopping**
- Completed trip: **Review spending**

### Principle C — Optimise for phone use during shopping

Planning may happen on desktop; shopping almost certainly happens on mobile. The grocery checklist must be highly touch-friendly:

- large check targets;
- sticky spending summary;
- category collapses;
- quick price entry;
- no tiny table columns;
- preserve progress after navigation or refresh.

### Principle D — Explain calculations without friction

Whenever cost changes, users should understand why. Provide expandable explanations, for example:

```text
Estimated list: 54,30 €
Saved using pantry: −12,10 €
Manual extras: +4,20 €
```

### Principle E — Avoid setup fatigue

A new user should not need to enter 50 ingredients before seeing value. Supply demo/seed ingredient data in development and provide a short onboarding path in the product:

- set budget;
- choose or create two recipes;
- place them into the week;
- generate first shopping list.

### Principle F — Calm modern design, not decorative clutter

Use subtle colour, clear cards, meaningful whitespace and excellent hierarchy. Recipe photos are optional and should never be required to use core functionality.

---

# 4. Information architecture and navigation

## 4.1 Primary navigation

Desktop sidebar; mobile bottom navigation.

### Main navigation items

1. **Dashboard** — `/dashboard/`
2. **Planner** — `/planner/`
3. **Shopping** — `/shopping/`
4. **Recipes** — `/recipes/`
5. **Pantry** — `/pantry/`
6. **Insights** — `/insights/`

Secondary access through profile/settings menu:

- Household & budget settings
- Ingredients
- Stores
- Sign out

### Mobile bottom nav

Limit to five items for clarity:

- Home
- Plan
- Shop
- Recipes
- More

“More” exposes Pantry, Insights and Settings.

## 4.2 Navigation behaviours

- Selected navigation item is visually distinct and accessible with `aria-current="page"`.
- On mobile shopping mode, hide distracting navigation in favour of back link + progress/sticky cost panel.
- Week context should persist when navigating from planner to shopping or dashboard.

---

# 5. Modern UI design system

## 5.1 Technical UI constraint

Use Django server-rendered templates, Tailwind CSS through the CDN, and small vanilla JavaScript modules/scripts for progressive enhancements. Do not set up Node/Vite/Webpack in MVP.

## 5.2 Visual direction

**Mood:** modern, warm, quiet, practical, premium enough to feel like a real product.

Avoid:

- childish food illustrations everywhere;
- over-saturated green;
- dense accounting tables as main mobile UI;
- gradients on every component;
- excessive animations.

## 5.3 Colour tokens

Codex should encode these as Tailwind utility conventions or CSS custom properties in a small base stylesheet so styling remains consistent.

| Token | Use | Suggested value |
|---|---|---|
| `canvas` | application background | `#FAF9F6` warm off-white |
| `surface` | card/background | `#FFFFFF` |
| `surface-muted` | muted blocks | `#F3F4EF` |
| `text` | primary text | `#172019` |
| `text-muted` | secondary text | `#667064` |
| `primary` | buttons/selected elements | `#236345` forest green |
| `primary-hover` | hover | `#1C5038` |
| `accent` | meal/planning highlights | `#E68A52` terracotta |
| `success` | under budget/completed | `#238556` |
| `warning` | approaching budget | `#B97918` |
| `danger` | exceeded budget/destructive | `#B74444` |
| `border` | borders/dividers | `#E5E5DE` |

Use contrast that meets WCAG AA for text and interactive elements.

## 5.4 Typography

Use one modern readable sans-serif family loaded with a simple external font import or fall back cleanly:

- Preferred: `Inter` or `Plus Jakarta Sans`.
- Display headline: semibold/bold, controlled size, no exaggerated marketing typography.
- Body: comfortable line height.
- Monetary values: tabular numerals when possible (`font-variant-numeric: tabular-nums`).

Suggested hierarchy:

| Purpose | Style intent |
|---|---|
| Page title | 28–32 px desktop, 24 px mobile, semibold |
| Card headline | 16–18 px, semibold |
| Primary money value | 30–36 px, bold, tabular |
| Body | 14–16 px |
| Metadata | 12–13 px, muted |

## 5.5 Layout

### Desktop

- Fixed or sticky left sidebar around 240 px.
- Main content max width around 1280 px.
- Dashboard uses a balanced responsive card grid.
- Planner spans full main content width.

### Mobile

- Full-width content with 16 px side padding.
- Sticky bottom navigation except during dedicated shopping mode.
- Cards stack vertically.
- Avoid horizontal scrolling except an intentionally designed weekly day strip if needed.

## 5.6 Component style rules

### Buttons

- Primary: filled forest green, medium height, rounded-xl, visible focus ring.
- Secondary: white with border.
- Destructive: red text or subtle red surface; reserve filled danger for confirmed destructive action.
- On mobile, important page action may be full width.

### Cards

- White surfaces, 1 px soft border, rounded-2xl, subtle shadow only when useful.
- Cards should group one logical concept, not every single field.

### Inputs

- Minimum 44 px interactive height.
- Clear labels above inputs; placeholders are examples, not replacements for labels.
- Inline validation under the field.
- Currency inputs clearly show EUR suffix/prefix.
- Quantity and unit inputs appear together.

### Status pills

- Soft backgrounds and meaningful labels: `Under budget`, `Near limit`, `Over budget`, `In pantry`, `Purchased`, `Unplanned`.
- Never rely on colour alone.

### Progress indicators

Budget progress bar:

- green through normal usage;
- amber when estimated/actual spend reaches 85% of budget;
- red only above 100%;
- always show numerical amount and difference.

## 5.7 Motion

- Use very small transitions for hover, opening filter panels and checking grocery items.
- Respect reduced-motion settings.
- Avoid distracting celebratory animations in MVP.

---

# 6. Screen-by-screen UX specification

## 6.1 Authentication screens

### Purpose

Create confidence quickly and bring the user into planning.

### Register page

Fields:

- Name (optional or display name)
- Email/username depending on chosen authentication implementation
- Password
- Confirm password

Visual design:

- Clean split layout on desktop: short value statement on left, register card on right.
- Single card centred on mobile.
- Copy: “Plan meals. Shop with purpose. Stay on budget.”

After registration, route to onboarding rather than an empty dashboard.

## 6.2 Onboarding — three lightweight steps

### Step 1: Household

- Household name, e.g. “Our home”
- People usually eating meals: default servings, e.g. 2
- Optional adults/children counters for later personalisation

### Step 2: Weekly budget

- Grocery budget input in euros
- Small explanatory sentence: “Used to compare your planned meals and actual shopping.”
- Suggested shortcuts: `50 €`, `75 €`, `100 €`, `150 €`, but fully editable.

### Step 3: First action

Two routes:

- **Create my first recipe**
- **Use sample recipes** — seed a small starter collection for this household if product policy allows; in strict user-data mode, present templates the user explicitly imports.

After completion: route to current week planner with a clear prompt to add meals.

## 6.3 Dashboard (`/dashboard/`)

### Primary question answered

“How is this week going financially and practically?”

### Page header

- Greeting or “This week” heading.
- Current week date range, with previous/next week navigation.
- Primary CTA changes with state:
  - no plan: `Plan this week`;
  - planned but no list: `Build shopping list`;
  - open list: `Continue shopping`;
  - completed trip: `Review spending`.

### Top summary grid

1. **Weekly budget card**
   - actual spend if purchases exist, otherwise estimated spend;
   - budget progress bar;
   - remaining or exceeded amount.

2. **Meals planned card**
   - count of occupied lunch/dinner slots;
   - next planned meal;
   - link to planner.

3. **Shopping card**
   - missing/purchased item counts;
   - estimated or actual list total;
   - link to shopping flow.

4. **Pantry saving card**
   - count of needs covered by pantry;
   - estimated savings when price data exists;
   - link to pantry.

### Secondary content

- Today/tomorrow meals list.
- “Where your spend changed” explanation when actual purchases exist:
  - planned shopping total;
  - manual extras;
  - difference between estimated and actual prices.
- Minimal insight list rather than complicated chart in early MVP.

### Empty dashboard state

A friendly, practical card:

```text
Plan your first week
Choose meals, see what you need to buy, and know your estimated cost before shopping.
[Plan this week]
```

## 6.4 Weekly planner (`/planner/?week=YYYY-MM-DD`)

### Page header

- Week selector and date range.
- Budget chip always visible.
- Primary action: `Generate shopping list` once at least one recipe meal exists.

### Desktop layout

A seven-column weekly board. Each day column contains:

- day label/date;
- lunch slot;
- dinner slot.

A slot has three states:

1. Empty: dashed add surface `+ Add meal`.
2. Recipe: recipe name, servings, cost estimate, tag and edit/remove menu.
3. Note-only: “Eating out”, “Leftovers”, etc.; clearly marked as non-calculated.

### Mobile layout

Do not compress seven columns into unusable cards. Use:

- a horizontal date selector/chip row for the week;
- one selected day’s lunch/dinner cards below;
- fast previous/next day movement;
- week estimated total sticky footer or header summary.

### Add meal interaction

Clicking `Add meal` opens a modal or slide-over:

- search recipes;
- filter tags (`Quick`, `Budget-friendly`, `Vegetarian`);
- show recipe cost per serving and time;
- select servings with increment/decrement controls;
- assign to slot.

Include a secondary option: `Add note instead`, such as restaurant, invited elsewhere, leftovers.

### Planner summary panel

Desktop: side or top panel. Mobile: collapsible compact panel.

Show:

- meals planned count;
- estimated ingredients cost before pantry deduction;
- pantry-covered estimated value after list generation where available;
- estimated shopping total;
- budget remaining/exceeded;
- link to explain calculation.

### Important interaction constraint

Do not implement drag-and-drop in the first release. Selection and edit controls are more reliable, accessible and simpler to test.

## 6.5 Recipe library (`/recipes/`)

### Purpose

Fast selection and reuse, not a social feed.

### Header

- Title `Recipes`
- Primary action `New recipe`
- Search input
- Filter chips: favourites/future; MVP tags; max preparation time optional.

### Cards

Each recipe card shows:

- recipe name;
- servings;
- cooking/prep time;
- estimated cost total and per serving where data exists;
- tag pills;
- actions: `Add to plan`, `View`, overflow edit/archive.

Use a list/card toggle only later if necessary; one responsive card grid/list is enough for MVP.

### Empty state

Explain why recipes matter for budgets and offer `Create recipe` plus optionally `Import sample recipes`.

## 6.6 Recipe create/edit (`/recipes/new/`, `/recipes/<id>/edit/`)

### Form structure

Use a multi-section form on one page, not an overcomplicated wizard:

1. **Basics**
   - name
   - short description
   - default servings
   - prep time and cooking time
   - tags

2. **Ingredients**
   - dynamic repeatable rows: ingredient, quantity, unit, optional note
   - button `Add ingredient`
   - allow creation of a missing ingredient through a small secondary modal/flow

3. **Instructions**
   - ordered steps textarea or repeatable steps; choose simplest robust MVP option: one textarea that supports numbered lines.

4. **Cost preview**
   - estimate calculated from known ingredient prices;
   - identify ingredients with no price so user understands incomplete estimate.

### Save controls

- Sticky save bar on long mobile form.
- `Save recipe` primary, `Cancel` secondary.
- After save, route to recipe detail or previous planner action context.

### Validation

- Name required.
- Default servings positive integer.
- At least one ingredient required.
- Quantity strictly greater than zero.
- Units valid for ingredient/base dimension.

## 6.7 Recipe detail (`/recipes/<id>/`)

Show:

- name, tags, time, servings;
- estimated total cost / per-serving cost;
- ingredients grouped plainly;
- instructions;
- CTA `Add to this week`;
- edit/archive actions.

## 6.8 Pantry (`/pantry/`)

### Core use

The user quickly records what is already available before generating the list.

### Desktop/mobile design

- Header: title and `Add pantry item`.
- Search and category filter.
- Compact item cards/rows with:
  - ingredient name;
  - amount remaining and unit;
  - optional expiry/best-before label;
  - edit quantity / remove controls.

### Fast quantity update

Do not require entering an edit page for every item. Offer a compact edit interaction/modal for quantity update.

### Empty state

```text
Your pantry reduces unnecessary shopping.
Add basics you already have, such as rice, pasta or oil.
[Add pantry item]
```

### MVP behaviour

Pantry stock is used when generating a list, but do not automatically permanently consume pantry stock merely because a meal was planned. Any deduction/consumption workflow should be explicitly confirmed or deferred to a later version.

## 6.9 Grocery list overview (`/shopping/` or `/shopping/lists/<id>/`)

### Entry states

1. No grocery list for selected week: CTA `Generate from meal plan`.
2. Draft generated list: user reviews items and estimates.
3. Shopping in progress: mobile-first checklist mode.
4. Completed: spending summary and optional adjustment actions.

### Draft grocery list layout

Header summary:

- week;
- number of meals generating needs;
- estimated list total;
- pantry-covered items/value;
- budget comparison.

Items grouped by category with:

- needed quantity;
- pantry deduction explanation if partially covered;
- expected purchase quantity;
- estimated price;
- remove/skip or edit action;
- `Add item` for snacks or household items not generated by meals.

Manual additions must be clearly labelled `Extra` so analytics can separate them.

Primary action: `Start shopping`.

## 6.10 Shopping mode — especially important UX (`/shopping/lists/<id>/shop/`)

This is one of the product's most valuable screens. It must feel convenient on a phone.

### Screen structure

#### Sticky header

- Back to list link;
- store selector/name optionally editable;
- progress: `5 of 12 picked`;
- live actual spend and budget remaining.

#### Category sections

- Collapsible categories: Vegetables, Dairy, Pantry, etc.
- Items appear as large touch rows.

#### Item row behaviour

Unchecked row:

```text
[ ] Chicken breast                       600 g
    Est. 6,90 €                         Planned
```

On check/tap, open a lightweight bottom sheet/modal or inline expansion:

- actual total price input (required to include in actual spend; allow “add later” state);
- actual quantity optional in MVP unless different quantity matters;
- status: purchased / unavailable / skipped;
- save and return to list.

Checked row visually de-emphasised but remains editable.

#### Quick add during shopping

Persistent or accessible `+ Add extra` button for unplanned items:

- name;
- category;
- actual price;
- optional quantity.

These items appear with `Extra` status and count toward actual spend.

#### Completion

Button `Finish trip` becomes available when user chooses to finish; do not require all planned items to be checked because items may be skipped/unavailable.

On finish, show confirmation summary:

- purchased total;
- items skipped/unpriced;
- planned estimate vs actual;
- budget remainder/overspend;
- manual extras total;
- CTA `Review week`.

## 6.11 Insights (`/insights/`)

### MVP insight design

Do not build fake rich analytics before there is enough real data. For one week, give understandable summary cards and breakdowns.

Filters:

- selected week; later month selector.

MVP sections:

1. Budget outcome: estimate, actual, difference.
2. Planned vs extras: how much actual spend came from generated needs versus manual additions.
3. Recipe cost summary: most/least expensive planned recipe estimates when fully priced.
4. Price accuracy: estimated versus actual grocery list difference where possible.

Empty state:

```text
Insights appear after you finish a shopping trip.
Plan meals and record actual prices to understand your spending.
```

## 6.12 Household/settings (`/settings/household/`)

Fields:

- household name;
- default servings;
- adults/children optional context;
- default weekly budget;
- currency fixed to EUR in MVP;
- week start fixed to Monday in MVP.

Confirm destructive changes or avoid them entirely in MVP.

---

# 7. Key workflows and user stories

## 7.1 First-use happy path

**Given** a newly registered user  
**When** they complete household setup with two servings and a budget of `80,00 €`, add/import recipes, plan meals, and generate a shopping list  
**Then** they see a real estimated list total and clear remaining budget status without needing to understand application internals.

## 7.2 Planning within budget

**Given** a weekly budget and recipe cost estimates  
**When** the user adds meals to the week  
**Then** the planner updates the estimated total and indicates whether they are comfortably under, near or over the budget.

## 7.3 Pantry-aware list

**Given** planned meals require `1000 g` of rice and the pantry records `400 g` rice  
**When** the shopping list is generated  
**Then** the list requires `600 g` rice, and explains that `400 g` is already at home.

## 7.4 Actual shopping truth

**Given** a list estimated at `60,00 €` and a shopping trip containing planned items totalling `63,00 €` plus `8,00 €` extras  
**When** the user finishes the trip  
**Then** the dashboard displays actual spending of `71,00 €`, estimate difference of `+11,00 €`, and separately identifies `8,00 €` as extras.

## 7.5 Re-plan without corrupting purchases

**Given** a completed shopping trip for a week  
**When** the meal plan changes later  
**Then** historical actual purchase records remain unchanged; the app may offer to regenerate a draft for missing new needs, but never silently rewrite completed spending history.

---

# 8. Business rules and calculation behaviour

## 8.1 Money

- Use Python `Decimal` and PostgreSQL numeric/decimal fields, never binary floating point, for prices and costs.
- Use 2 decimal places for stored monetary amounts.
- All totals are computed server-side; JavaScript may preview but cannot be the source of truth.
- Price values cannot be negative.
- Display in EUR for MVP.

## 8.2 Quantities and units

### MVP units

| Dimension | Units | Canonical storage unit |
|---|---|---|
| Weight | `g`, `kg` | `g` |
| Volume | `ml`, `l` | `ml` |
| Count | `unit` | `unit` |

- Store normalised quantity in canonical unit for calculations.
- Preserve user display unit or convert cleanly when rendering.
- Do not combine incompatible dimensions, e.g. `unit` eggs with `g` eggs, unless an explicit conversion is added later.
- Quantity values must be positive for recipe rows and purchases; pantry quantity may reach zero and then the item may be removed or marked empty.

## 8.3 Ingredient price model for MVP

Generic ingredient prices are estimated prices, not guaranteed store product prices.

Recommended initial model:

- Each household can store an estimated price for an ingredient in a chosen price basis, e.g. `rice: 2.20 € per kg`, `eggs: 2.80 € per 6 units` if packaging is supported, or simplify MVP to a canonical-unit price.
- For robust first implementation, store price per canonical unit with sensible UI conversion, while avoiding exposing awkward values such as price per gram. UI can ask user for `price` and `package quantity/unit`, then compute price per canonical unit.
- If an ingredient lacks price data, cost estimates are marked incomplete and the UI lists missing prices rather than pretending the total is complete.

## 8.4 Recipe cost calculation

- Scale recipe ingredient quantities according to planned servings:

```text
scaled_required_quantity = base_recipe_quantity × planned_servings / recipe_default_servings
```

- Estimated recipe cost is the sum of priced scaled ingredients.
- Show a “partial estimate” label if any ingredient price is missing.
- Cost per serving uses planned or default servings as appropriate.

## 8.5 Grocery aggregation

For a plan/week:

1. Include recipe ingredients for all calculated planned meals.
2. Scale each recipe occurrence by its servings.
3. Normalise compatible units to canonical units.
4. Group by ingredient.
5. Sum required quantities.
6. Deduct available pantry quantity up to total required amount.
7. Shopping required quantity is never less than zero.
8. Include manual extra grocery items separately.

## 8.6 Pantry behaviour

- Planning does not automatically consume pantry stock.
- Generated grocery list records the pantry coverage calculation as a snapshot/explanation.
- Later versions may add a confirmed “cook/consume” action.
- When a grocery list is regenerated before shopping begins, the current draft calculation can update.
- After shopping begins or a trip is completed, do not silently overwrite actual lines.

## 8.7 Budget states

Suggested classification:

| State | Rule | UI label |
|---|---|---|
| No estimate | No sufficient price data | `Complete prices to estimate` |
| Healthy | spend < 85% budget | `Under budget` |
| Near limit | spend >= 85% and <= 100% | `Near budget limit` |
| Over | spend > budget | `Over budget` |

Use estimated spending before a shopping trip is completed; use actual spending after actual purchases are present, while keeping both visible.

## 8.8 Weekly time rules

- A meal plan belongs to a household and a Monday week-start date.
- Enforce one main meal plan per household per week in MVP.
- Planned meal slots: unique combination of meal plan, date and meal type (`lunch`, `dinner`).
- A note-only slot may exist without recipe and has no generated cost.

---

# 9. Technical architecture

## 9.1 Required stack

- Python: supported modern stable version; record selected version in README.
- Django: current stable release chosen at project creation; pin dependencies.
- PostgreSQL.
- HTML via Django templates.
- Tailwind CSS via CDN for MVP.
- Vanilla JavaScript only for interactive UI enhancements.
- Tests: `pytest` plus `pytest-django` preferred for readable TDD workflow, unless project baseline already uses Django TestCase consistently.
- Environment variables for secrets/database settings.

## 9.2 Architectural style

Use a conventional Django monolith with clear domain apps. This is deliberately not microservices. The complexity is in correct domain rules and excellent usability.

Suggested project shape:

```text
mealbudget/
├── manage.py
├── config/                       # Django project settings, URL config, WSGI/ASGI
├── core/                         # home redirect, shared utilities, template tags, base views
├── accounts/                     # auth/onboarding ownership glue if needed
├── households/                   # households and recurring budget preferences
├── recipes/                      # ingredients, tags, recipes, recipe ingredients
├── planning/                     # weeks, planned meal slots, grocery-generation initiation
├── pantry/                       # pantry stock
├── shopping/                     # grocery lists, list lines, trips, purchased/extra lines
├── insights/                     # query/services/views for summaries; limited models if any
├── templates/
│   ├── base.html
│   ├── components/
│   └── ... app templates
├── static/
│   ├── css/app.css                # CSS variables and very small custom rules
│   ├── js/app.js
│   ├── js/planner.js
│   └── js/shopping.js
├── tests/ or app-level tests/
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   └── DECISIONS.md
├── AGENTS.md
├── .env.example
├── requirements.txt or pyproject.toml
└── README.md
```

Codex may adapt app boundaries if it documents a better simpler choice, but it must keep domain responsibilities separate and avoid a single giant app.

## 9.3 Service-layer rule

Views coordinate HTTP concerns; forms validate user input; services execute important use cases; selectors/query helpers assemble display data.

Important business logic must be in testable Python functions/services, for example:

```text
recipes/services/costing.py
    calculate_recipe_estimate(...)

planning/services/grocery_generation.py
    aggregate_required_ingredients(...)
    generate_grocery_list_for_plan(...)

shopping/services/trips.py
    start_trip(...)
    complete_trip(...)
    calculate_spending_breakdown(...)

pantry/services/availability.py
    calculate_pantry_coverage(...)
```

Exact module paths may differ; responsibility separation is mandatory.

## 9.4 Server-rendered interaction strategy

- Standard Django POST/Redirect/GET for durable actions.
- Vanilla JavaScript enhances repeated recipe ingredient rows, modals, mobile day selection, checkbox interactions and live display previews.
- Core actions must still be robust when JavaScript fails where reasonably practical.
- No API-first architecture is required for MVP; JSON endpoints may be added only for clearly justified progressive interactions.

---

# 10. Proposed data model

Names below are recommendations; Codex may adjust naming only with rationale recorded in `docs/DECISIONS.md`.

## 10.1 Household and budget

### `Household`

| Field | Notes |
|---|---|
| `id` | primary key |
| `owner` | FK to authenticated user; MVP one owner |
| `name` | required |
| `default_servings` | positive integer, default 2 |
| `adults_count` | optional/context, non-negative |
| `children_count` | optional/context, non-negative |
| `default_weekly_budget` | Decimal, positive |
| `currency` | default `EUR`, fixed UI in MVP |
| `created_at`, `updated_at` | timestamps |

### `WeeklyBudget` or budget snapshot on `MealPlan`

Decision point: each week must preserve the budget applied to it even if household default later changes. The simplest robust approach is a `budget_amount` Decimal stored on `MealPlan`, initialised from household default when created.

## 10.2 Recipes and ingredients

### `Ingredient`

| Field | Notes |
|---|---|
| `household` | scoped to household for MVP; future global catalogue possible |
| `name` | required, case-insensitive uniqueness within household ideally |
| `category` | controlled choices |
| `canonical_unit` | `g`, `ml`, or `unit` |
| `price_amount` | nullable Decimal estimate entered by user |
| `price_quantity` | nullable Decimal > 0 |
| `price_unit` | compatible unit; converted for costing |
| `is_archived` | prevents breaking historical records |

### `Recipe`

| Field | Notes |
|---|---|
| `household` | owner household |
| `name` | required |
| `description` | short optional text |
| `default_servings` | positive integer |
| `prep_minutes` | nullable non-negative integer |
| `cook_minutes` | nullable non-negative integer |
| `instructions` | text |
| `is_archived` | Boolean |
| `created_at`, `updated_at` | timestamps |

### `RecipeTag`

Could use fixed choices through a many-to-many or a simple tags model. Keep MVP modest and easy to query.

### `RecipeIngredient`

| Field | Notes |
|---|---|
| `recipe` | FK |
| `ingredient` | FK |
| `quantity` | positive Decimal |
| `unit` | compatible with ingredient canonical unit |
| `note` | optional, e.g. diced |
| `position` | ordering |

## 10.3 Planning

### `MealPlan`

| Field | Notes |
|---|---|
| `household` | FK |
| `week_start` | Monday date |
| `budget_amount` | Decimal snapshot for this week |
| `created_at`, `updated_at` | timestamps |

Constraint: unique `(household, week_start)`.

### `PlannedMeal`

| Field | Notes |
|---|---|
| `meal_plan` | FK |
| `date` | within plan week |
| `meal_type` | `lunch` or `dinner` |
| `recipe` | nullable FK for note-only slot |
| `servings` | nullable/required when recipe set |
| `note` | optional text |

Constraint: unique `(meal_plan, date, meal_type)`.

## 10.4 Pantry

### `PantryItem`

| Field | Notes |
|---|---|
| `household` | FK |
| `ingredient` | FK |
| `quantity` | non-negative Decimal |
| `unit` | compatible unit |
| `best_before_date` | optional future-use field okay in MVP UI if easy |
| `updated_at` | timestamp |

Constraint: one active item per household/ingredient in MVP unless batch/expiry complexity is explicitly added later.

## 10.5 Shopping

### `GroceryList`

| Field | Notes |
|---|---|
| `meal_plan` | one-to-one or FK if list versions are required; simplest MVP one active list |
| `status` | `draft`, `shopping`, `completed` |
| `generated_at` | timestamp |
| `started_at`, `completed_at` | nullable timestamps |
| `store_name` | optional text in MVP |

### `GroceryListItem`

| Field | Notes |
|---|---|
| `grocery_list` | FK |
| `ingredient` | nullable for free-form extras if needed; ideally ingredient can be created/selected |
| `label` | display label snapshot |
| `category` | category snapshot or relationship-derived |
| `required_quantity` | amount recipes require; nullable for extras |
| `pantry_covered_quantity` | amount already at home |
| `quantity_to_buy` | generated result or manual quantity |
| `unit` | unit |
| `source` | `planned` or `extra` |
| `estimated_cost` | nullable Decimal |
| `actual_cost` | nullable Decimal |
| `actual_quantity` | nullable Decimal |
| `status` | `pending`, `purchased`, `skipped`, `unavailable` |
| `position` | optional ordering |

MVP may store actual purchase fields on the list item rather than introduce a separate purchase line entity; Codex should decide with an eye on preserving completed trips and future history. If separating `ShoppingTrip`/`PurchaseItem` provides clearer history without needless complexity, document and adopt it.

---

# 11. Routes and page responsibilities

The exact route namespace may change, but user-facing behaviour must be coherent.

| Page/action | Suggested route | Purpose |
|---|---|---|
| Register | `/accounts/register/` | create user |
| Login/logout | Django auth routes | authenticate |
| Onboarding | `/onboarding/` | create household/default budget |
| Dashboard | `/dashboard/` | current week summary |
| Planner | `/planner/` | default current week |
| Planner selected week | `/planner/?week=YYYY-MM-DD` | inspect/edit selected week |
| Add/edit meal slot | `/planner/<plan_id>/slots/...` | durable action/modal-backed form |
| Recipes | `/recipes/` | library |
| Recipe detail/new/edit | `/recipes/<id>/`, `/recipes/new/`, `/recipes/<id>/edit/` | recipe management |
| Ingredients/settings | `/ingredients/` | manage pricing/catalogue |
| Pantry | `/pantry/` | available ingredients |
| Generate list | `/planner/<id>/generate-shopping-list/` | POST action |
| Shopping list | `/shopping/lists/<id>/` | review generated list |
| Shopping mode | `/shopping/lists/<id>/shop/` | phone-first purchase entry |
| Finish trip | `/shopping/lists/<id>/complete/` | POST finalise |
| Insights | `/insights/` | spending summaries |
| Household settings | `/settings/household/` | budget/profile |

All household-owned objects must be filtered by the authenticated user's household; never allow ID guessing to expose another household's data.

---

# 12. Template/component architecture

## 12.1 Base templates

- `templates/base.html`: global head, Tailwind CDN configuration/theme extension, fonts, CSS, app shell.
- `templates/layouts/app_shell.html`: authenticated sidebar/bottom nav layout.
- `templates/layouts/auth_shell.html`: login/register/onboarding layout.

## 12.2 Reusable UI partials

Create reusable templates/partials rather than duplicating markup:

```text
templates/components/
├── button.html or consistent utility macros/partials approach
├── budget_progress.html
├── money_value.html
├── status_pill.html
├── empty_state.html
├── page_header.html
├── form_field.html where useful
├── modal_shell.html
├── recipe_card.html
├── meal_slot_card.html
├── grocery_item_row.html
└── mobile_bottom_nav.html
```

Django does not require a component framework; use includes cleanly. Do not create abstraction so elaborate that small changes become difficult.

## 12.3 Copy tone

Copy should be short, practical and friendly:

- Prefer: “You have 18,20 € left in this week’s plan.”
- Avoid: “Budget utilisation ratio computation successful.”
- Prefer: “Add what you already have to avoid buying it twice.”
- Avoid guilt-inducing language when over budget.

---

# 13. JavaScript enhancements

Use small separate vanilla JavaScript files. Avoid large inline scripts in templates.

## 13.1 MVP JS behaviours

- Dynamic recipe ingredient form rows using Django formsets or an equivalent robust approach.
- Mobile planner day switcher.
- Modal/slide-over controls for adding a meal if implemented without full page navigation.
- Shopping checklist interaction and price-entry reveal.
- Sticky/live client-side preview total while entries are typed; server recomputes after submit.
- Accessible dismissal/toggle behaviours.

## 13.2 Progressive enhancement rule

- Server validations are authoritative.
- Important state changes use forms/POST endpoints and CSRF protection.
- Do not store the only copy of shopping state in browser local storage.

---

# 14. Accessibility and usability requirements

Codex must consider these as acceptance requirements, not optional polish:

- Semantic HTML landmarks and heading hierarchy.
- All form controls have labels.
- Keyboard-accessible interactive controls and modals.
- Visible focus rings.
- Minimum practical tap target around 44×44 px on shopping mode controls.
- Colour is never the sole indicator of budget or item status.
- Modals, if used, manage focus and close accessibly; a full-page form is acceptable when modal complexity would harm quality.
- Messages/forms preserve useful entered values after validation errors.
- Mobile screens should not require horizontal table scrolling for routine tasks.

---

# 15. Security, correctness and data integrity

## 15.1 Security baseline

- Use Django authentication and CSRF protections.
- All non-public pages require login.
- Scope all user data by owned household.
- No secrets committed; use `.env.example`.
- Validate and sanitise form inputs through Django forms.
- Avoid raw SQL unless truly justified and parameterised.

## 15.2 Data integrity constraints

- Unique household/week plan.
- Unique meal slot per plan/date/type.
- Positive recipe quantities and servings.
- Positive budget and non-negative actual costs.
- Unit compatibility enforced in services/forms and, where appropriate, model validation.
- Archived recipes/ingredients remain referentially valid for historical weeks.

## 15.3 Performance expectations for MVP

- Use appropriate `select_related`/`prefetch_related` for planner, recipe and shopping screens.
- Avoid N+1 queries in weekly dashboard and grocery generation.
- No premature caching.
- Use database transactions for generation/completion workflows that update multiple rows.

---

# 16. TDD test specification

## 16.1 Test framework and organisation

Preferred tooling:

- `pytest`
- `pytest-django`
- factories only if they clearly reduce repetitive test setup; do not overbuild fixture infrastructure early.

Test naming should describe behaviour. Separate tests by domain and feature.

## 16.2 Mandatory domain tests before UI sophistication

### Units

- converts kg to g correctly;
- converts l to ml correctly;
- refuses incompatible unit combinations;
- preserves Decimal precision.

### Recipe costing

- computes full estimate when all ingredient prices exist;
- reports incomplete estimate when a price is missing;
- scales ingredients and estimate when servings differ from recipe default;
- computes cost per serving correctly.

### Meal plan

- creates one plan for a household/week;
- rejects duplicate slot for same date/type;
- restricts slot date to selected week;
- note-only meal adds no ingredient requirement.

### Grocery generation

- aggregates same ingredient from several meals;
- applies serving scaling before aggregation;
- deducts full pantry coverage;
- deducts partial pantry coverage;
- never generates a negative quantity;
- separates manual extras from planned items;
- regenerates a draft list consistently;
- does not overwrite completed trip/spending history.

### Budget calculations

- classifies under-budget, near-limit and over-budget values;
- displays/returns no-estimate state when pricing is incomplete;
- separates estimated and actual totals;
- attributes extra purchases separately.

### Authorisation

- unauthenticated user redirected from private pages;
- one household user cannot access/edit another household's plan, recipe, pantry or list.

## 16.3 View/integration tests

At minimum:

1. Registration/onboarding creates household and routes to planner.
2. Create ingredient and recipe through forms.
3. Assign recipe to planned meal.
4. Generate list and render expected quantities.
5. Update shopping item actual price and complete list.
6. Dashboard displays actual spend/budget result.

## 16.4 UI manual verification checklist

For visually significant changes, Codex should provide a checklist for the user to inspect:

- desktop at common width;
- phone/narrow width;
- keyboard navigation/focus visibility;
- empty state;
- validation error state;
- over-budget state;
- shopping mode interaction.

No need for automated browser tests in the very first slice unless Codex already has a reliable configured harness; introduce them later when core flow stabilises.

---

# 17. Seed/demo data for development

Provide a management command or fixture to create a local demo household/data set, without contaminating production data.

Suggested ingredients with plausible placeholder estimate values expressly labelled demo values:

- rice, pasta, potatoes, onion, tomatoes, carrots, lentils;
- chicken breast, ground beef, eggs;
- milk, grated cheese, yoghurt;
- olive oil, coconut milk, tomato sauce.

Suggested recipes:

- Lentil soup — budget-friendly, vegetarian, batch-cook.
- Chicken rice bowl — family-friendly.
- Pasta bolognese — family-friendly.
- Vegetable curry — vegetarian, quick.
- Omelette with potatoes — budget-friendly, quick.

Seed data helps develop the UX; it must never be represented as live price truth.

---

# 18. Implementation roadmap: vertical slices

Codex should not skip straight to future features. Maintain status in `docs/IMPLEMENTATION_PLAN.md`.

## Phase 0 — Repository foundation and design shell

### Goal

A running Django/PostgreSQL project with test tooling and a coherent modern UI shell.

### Deliverables

- Project initialisation and pinned dependencies.
- PostgreSQL environment configuration and `.env.example`.
- Base settings, static/templates structure.
- Tailwind CDN configured with design tokens.
- Auth pages shell and authenticated app shell/sidebar/mobile nav.
- Placeholder dashboard page accessible after login.
- `AGENTS.md`, README, docs plan/decisions.
- Test configuration and initial smoke tests.

### Definition of done

- Project boots locally from documented commands.
- Tests run successfully.
- Login-protected dashboard renders in modern responsive shell.

## Phase 1 — Household onboarding and weekly budget

### Goal

A new user reaches a useful personalised weekly context.

### Deliverables

- Registration/login/logout.
- Household model/settings.
- Onboarding flow and default budget.
- Current week helper/Monday week-start behaviour.
- Dashboard empty state and CTA to planner.
- TDD coverage for household ownership/budget validation.

## Phase 2 — Ingredients and recipe library

### Goal

Users can create cost-aware reusable meals.

### Deliverables

- Ingredients/catalogue/pricing model.
- Unit conversion utilities with tests.
- Recipe CRUD and dynamic ingredient rows.
- Recipe estimate service.
- Recipe library/detail UI with filters/tags basics.

## Phase 3 — Weekly planner

### Goal

A week can be filled with meals and costs understood.

### Deliverables

- MealPlan and PlannedMeal models.
- Planner desktop/mobile layouts.
- Add/edit/remove meal slot interactions.
- Servings-based recipe scaling and estimated weekly meal costs.
- Budget summary/warning state.

## Phase 4 — Pantry-aware grocery generation

### Goal

Turn planned meals into an accurate “what to buy” list.

### Deliverables

- Pantry CRUD UI.
- Grocery generation service and snapshots.
- Grocery list draft review screen.
- Pantry deductions visible to user.
- Missing-price explanation.

## Phase 5 — Mobile shopping mode and actual spend

### Goal

Use the application in a shop and record reality.

### Deliverables

- Start shopping / shopping mode / finish trip lifecycle.
- Touch-friendly checklist.
- Actual price entry.
- Manual extras.
- Completed spending immutability/protection.

## Phase 6 — Dashboard and insight refinement

### Goal

Make the weekly feedback loop clearly useful.

### Deliverables

- Real dashboard data cards.
- Planned versus actual breakdown.
- Extras and price-difference explanation.
- Recipe cost insight.
- Empty/loading/state polish and responsive QA.

## Later roadmap (not part of initial implementation unless requested)

- meal-plan duplication/favourites;
- leftovers;
- monthly insights and exports;
- collaborative households;
- Open Food Facts/barcodes;
- receipt import;
- suggestions/optimisation;
- i18n/PWA.

---

# 19. Detailed acceptance scenarios for MVP completion

Codex and the user should be able to use these as end-to-end acceptance checks.

## Scenario A — Plan and estimate a week

1. Sign up and create household with `2` default servings and `80,00 €` weekly budget.
2. Create ingredients with compatible prices.
3. Create at least two recipes.
4. Add recipes into three or more meal slots for current week.
5. Planner displays calculated estimated cost and budget status.

**Pass condition:** totals match server-side calculations and layout works on desktop/mobile.

## Scenario B — Pantry reduces required purchase

1. Add `500 g` rice to pantry.
2. Plan recipes requiring `800 g` rice total.
3. Generate grocery list.

**Pass condition:** rice line explains `800 g needed`, `500 g in pantry`, `300 g to buy`.

## Scenario C — Shopping records actual overspend clearly

1. Start shopping from generated list.
2. Mark planned items purchased with actual prices exceeding estimates.
3. Add an extra snack/item with actual cost.
4. Finish trip.

**Pass condition:** dashboard/summary separates planned estimate difference and extras, with actual total and budget outcome.

## Scenario D — Missing estimates are honest

1. Create recipe containing an ingredient without estimated price.
2. Plan it and generate grocery list.

**Pass condition:** interface does not show a misleading complete total; it flags missing price information and offers a path to complete it.

## Scenario E — Isolation and history

1. Two households exist in test setup.
2. User A attempts to access User B's recipe/list URLs.
3. Complete a shopping trip then modify planner.

**Pass condition:** cross-household access is denied/not found; completed purchase totals are not silently rewritten.

---

# 20. Decisions Codex must record rather than silently invent

Record chosen solution and reasoning in `docs/DECISIONS.md` for:

- chosen Python and Django versions;
- dependency management format (`requirements.txt` vs `pyproject.toml`);
- user identity choice (Django username vs email-oriented authentication);
- model for ingredient estimates and package quantities;
- whether actual purchase data lives on grocery list items or separate trip/purchase models;
- formset/JavaScript approach for dynamic recipe ingredients;
- app boundaries if they differ from this proposal;
- future i18n readiness approach.

---

# 21. Definition of Done for any Codex task

A feature task is done only when:

- behaviour is aligned with this specification or any documented later decision;
- tests were created/updated and pass;
- migrations are provided and safe where models changed;
- authorisation and household ownership have been considered;
- UI includes necessary empty/error/validation states for the implemented surface;
- the page is usable at narrow mobile width when it is user-facing;
- README/docs are updated if setup, workflow or design decisions changed;
- Codex reports exact verification commands and known remaining work.

---

# 22. Suggested first Codex task after planning approval

After Codex has analysed this spec and proposed a plan, the first implementation request should usually be:

> Implement Phase 0 only: initialise or align the Django/PostgreSQL foundation, testing harness, environment/configuration, shared UI shell and placeholder authenticated dashboard, following TDD where behaviour exists. Do not implement recipes, planner or shopping yet. Ensure the visual shell already reflects the design tokens and responsive navigation described in the specification.

This prevents uncontrolled code generation while ensuring the project starts with quality, UI coherence and test habits.

---

# 23. Final product quality bar

The MVP should look and behave like a purposeful modern web product, not a school CRUD exercise. Technical quality comes from tested money/quantity/business rules and secure ownership; product quality comes from making the weekly loop effortless:

```text
I choose meals → I know what to buy → I shop conveniently → I know what happened to my budget.
```

Every implementation choice should strengthen this loop.
