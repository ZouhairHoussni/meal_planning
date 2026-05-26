# MealBudget

MealBudget is a budget-first weekly meal planning and grocery tracking web application for euro/metric households.

This repository has the Django/PostgreSQL foundation plus an early compact product loop: signup, household onboarding with a weekly EUR budget, recipes with components, a draggable weekly planner, shopping items generated from planned recipes, manual grocery additions, a pantry page, and branded/admin-registered models.

## Stack

- Python 3.12
- Django 5.2.14 LTS
- PostgreSQL
- Server-rendered Django templates
- Tailwind CSS through CDN
- Vanilla JavaScript
- pytest and pytest-django

## Local Setup

1. Create and activate a virtual environment if desired.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and adjust values if needed.
4. Start PostgreSQL. With Docker available:

   ```powershell
   docker compose up -d db
   ```

5. Run migrations:

   ```powershell
   python manage.py migrate
   ```

6. Run the development server:

   ```powershell
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/dashboard/`.

## Current Workflows

- Sign up at `/accounts/signup/`.
- Set up a single owned household and weekly budget at `/household/onboarding/`.
- Edit household defaults and budget at `/household/settings/`.
- Create recipes at `/recipes/new/`.
- Drag recipes into breakfast, lunch, dinner or extra slots at `/planner/`.
- View generated planned shopping items and add manual groceries at `/shopping/`.
- Add or edit optional price, brand and store on shopping items.
- See known shopping spend totals, budget remaining, store spend and missing-price counts on Shopping and Dashboard.
- Add pantry items at `/pantry/`.
- Manage users, recipes, planner entries, pantry items and shopping items at `/admin/`.

## Verification

```powershell
python manage.py check
python -m pytest
```

The test database is expected to use PostgreSQL via `DATABASE_URL`.
