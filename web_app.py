from flask import Flask, render_template, request, redirect, url_for, json
from expense_logic import ExpenseTracker
from datetime import datetime

app = Flask(__name__)
tracker = ExpenseTracker()

CURRENCY = "VND"
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]

@app.route('/')
def index():
    # Get search/filter parameters from URL
    search_term = request.args.get('search', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    # Get filtered expenses
    if search_term or start_date or end_date or category_filter:
        all_expenses = tracker.search_expenses(
            search_term=search_term if search_term else None,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
            category=category_filter if category_filter else None
        )
    else:
        all_expenses = tracker.get_all_expenses()

    # Get available categories for filter dropdown
    available_categories = tracker.get_categories()
    
    category_totals = {}
    for expense in all_expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    category_labels = list(category_totals.keys())
    category_values = list(category_totals.values())

    monthly_totals = {}
    for expense in all_expenses:
        month = expense.date[:7] 
        monthly_totals[month] = monthly_totals.get(month, 0) + expense.amount
    
    # Sort by month to ensure correct order
    sorted_months = sorted(monthly_totals.keys(), reverse=True)
    # Get data for the last 6 months if available
    recent_months = sorted_months[:6]
    monthly_labels = list(reversed(recent_months))
    monthly_values = [monthly_totals[month] for month in monthly_labels]

    # --- Budget Information ---
    current_month_str = datetime.now().strftime("%Y-%m")
    budget = tracker.get_budget(current_month_str)
    total_spent_current_month = monthly_totals.get(current_month_str, 0)

    return render_template(
        'index.html', 
        expenses=all_expenses, 
        categories=CATEGORIES, 
        currency=CURRENCY,
        # Search/filter parameters
        search_term=search_term,
        start_date=start_date,
        end_date=end_date,
        category_filter=category_filter,
        available_categories=available_categories,
        # Data for charts
        category_labels=json.dumps(category_labels),
        category_values=json.dumps(category_values),
        monthly_labels=json.dumps(monthly_labels),
        monthly_values=json.dumps(monthly_values),
        # Budget data
        current_month=current_month_str,
        budget=budget,
        total_spent=total_spent_current_month
    )

@app.route('/set_budget', methods=['POST'])
def set_budget():
    try:
        budget_amount = float(request.form['budget_amount'])
        if budget_amount >= 0:
            current_month_str = datetime.now().strftime("%Y-%m")
            tracker.set_budget(current_month_str, budget_amount)
    except (ValueError, KeyError):
        # Ignore if the value is invalid or not provided
        pass
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    description = request.form['description']
    try:
        amount = float(request.form['amount'])
    except ValueError:
        # Handle case where amount is not a valid number, redirect home
        return redirect(url_for('index'))
        
    tracker.add_expense(category, description, amount)
    return redirect(url_for('index')) # Redirect back to the main page

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    tracker.delete_expense(expense_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:expense_id>', methods=['GET'])
def edit_expense_page(expense_id):
    expense = tracker.get_expense_by_id(expense_id)
    if not expense:
        return "Expense not found", 404
    
    return render_template(
        'edit.html',
        expense=expense,
        categories=CATEGORIES,
        currency=CURRENCY
    )

@app.route('/update/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    expense = tracker.get_expense_by_id(expense_id)
    if not expense:
        return "Expense not found", 404

    expense.date = request.form['date']
    expense.category = request.form['category']
    expense.description = request.form['description']
    expense.amount = float(request.form['amount'])
    
    tracker.update_expense(expense)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 
