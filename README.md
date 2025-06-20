# Expense Tracker

A simple and elegant Expense Tracker web application built with Python, Flask, and SQLite. This application helps users track their daily expenses, visualize spending habits through charts, and manage monthly budgets.

![Expense Tracker Screenshot](https://i.imgur.com/your-screenshot-url.png)  <!-- You can replace this with a real screenshot URL later -->

## Features

- **Add, Edit, Delete Expenses:** Full CRUD (Create, Read, Update, Delete) functionality for managing expenses.
- **SQLite Database:** Uses a lightweight and reliable SQLite database to store data.
- **Data Visualization:**
    - A pie chart showing the distribution of expenses by category.
    - A bar chart showing the spending trend over the last few months.
- **Search & Filter:**
    - Search for expenses by description.
    - Filter expenses by a specific category.
    - Filter expenses within a date range.
- **Monthly Budgeting:**
    - Set a budget for the current month.
    - A progress bar visually tracks spending against the budget.
- **Clean UI:** A clean and modern user interface built with [Pico.css](https://picocss.com/).

## Technologies Used

- **Backend:**
    - Python
    - Flask
    - SQLite3
- **Frontend:**
    - HTML5
    - Pico.css
    - JavaScript
    - Chart.js

## How to Run Locally

Follow these steps to get the application running on your local machine.

### Prerequisites

- Python 3.x installed on your system.
- `pip` for package management.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sangoonthego/Expense_Tracker.git
    cd Expense_Tracker
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\\Scripts\\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    The only external library required is Flask.
    ```bash
    pip install Flask
    ```

4.  **Run the application:**
    ```bash
    python web_app.py
    ```

5.  **Open your browser:**
    Navigate to `http://127.0.0.1:5000` to see the application in action. The `expenses.db` file will be created automatically on the first run.

## Project Structure
```
Expense_Tracker/
├── expense_logic.py    # Handles all database interactions and business logic.
├── web_app.py          # The main Flask application file.
├── expenses.db         # The SQLite database file (created on run).
├── static/
│   ├── css/
│   │   └── style.css   # Custom CSS styles.
│   └── js/
│       └── charts.js   # JavaScript for rendering charts.
└── templates/
    ├── index.html      # Main page template.
    └── edit.html       # Template for editing an expense.
```
