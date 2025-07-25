# Personal Finance Tracker

A Django-based web application to help users track their personal finances, manage budgets, and visualize their financial data.

## Features

1. Add, update, and delete income and expense entries
2. Categorize expenses (food, transportation, entertainment, etc.)
3. Generate monthly and yearly financial summaries
4. Visualize income vs. expenses over time with graphs
5. Set budget limits and receive alerts

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ to access the application

## Project Structure

- `finance_tracker/` - Main project directory
  - `accounts/` - User authentication and profile management
  - `transactions/` - Income and expense management
  - `budgets/` - Budget tracking and alerts
  - `reports/` - Financial reports and visualizations
  - `templates/` - HTML templates
  - `static/` - CSS, JavaScript, and other static files 