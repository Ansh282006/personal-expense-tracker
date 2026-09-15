from flask import Flask, render_template, request, redirect, url_for
from src.database import init_db, add_expense, get_all_expenses

# Explicitly tell Flask where templates and static folders are
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize the database when the app starts
init_db()


@app.route('/')
def index():
    """Home page - displays all expenses."""
    expenses = get_all_expenses()
    total = sum(expense[2] for expense in expenses) if expenses else 0.0
    return render_template('index.html', expenses=expenses, total=total)


@app.route('/add', methods=['POST'])
def add():
    """Handles the form submission to add a new expense."""
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form.get('description', '')
    add_expense(amount, category, description)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)