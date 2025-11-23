#!/usr/bin/env python3
"""
Flask web application for Expense Tracker
"""

from flask import Flask, render_template, request, jsonify
from expense_tracker import ExpenseTracker
import os

app = Flask(__name__)
tracker = ExpenseTracker()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses, optionally filtered"""
    category = request.args.get('category', None)
    month = request.args.get('month', None)
    
    filtered_expenses = tracker.expenses
    
    if category:
        filtered_expenses = [e for e in filtered_expenses if e.category.lower() == category.lower()]
    
    if month:
        filtered_expenses = [e for e in filtered_expenses if e.date.startswith(month)]
    
    # Sort by date (newest first)
    filtered_expenses.sort(key=lambda x: x.date, reverse=True)
    
    expenses_data = [exp.to_dict() for exp in filtered_expenses]
    total = sum(exp.amount for exp in filtered_expenses)
    
    return jsonify({
        'expenses': expenses_data,
        'total': total,
        'count': len(expenses_data)
    })


@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """Add a new expense"""
    data = request.json
    
    description = data.get('description', '').strip()
    amount = data.get('amount', 0)
    category = data.get('category', '').strip()
    date = data.get('date', '').strip() or None
    
    if not description:
        return jsonify({'success': False, 'error': 'Description cannot be empty'}), 400
    
    if not category:
        return jsonify({'success': False, 'error': 'Category cannot be empty'}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'error': 'Amount must be greater than 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400
    
    success = tracker.add_expense(description, amount, category, date)
    
    if success:
        return jsonify({'success': True, 'message': 'Expense added successfully!'})
    else:
        return jsonify({'success': False, 'error': 'Failed to save expense'}), 500


@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense"""
    success = tracker.delete_expense(expense_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Expense deleted successfully!'})
    else:
        return jsonify({'success': False, 'error': 'Expense not found'}), 404


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get expense statistics"""
    if not tracker.expenses:
        return jsonify({
            'total': 0,
            'count': 0,
            'average': 0,
            'categories': {}
        })
    
    total = sum(e.amount for e in tracker.expenses)
    category_totals = {}
    
    for expense in tracker.expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    
    # Calculate percentages
    category_data = {}
    for category, amount in category_totals.items():
        percentage = (amount / total) * 100 if total > 0 else 0
        category_data[category] = {
            'amount': amount,
            'percentage': round(percentage, 1)
        }
    
    return jsonify({
        'total': total,
        'count': len(tracker.expenses),
        'average': total / len(tracker.expenses) if tracker.expenses else 0,
        'categories': category_data
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    categories = sorted(set(e.category for e in tracker.expenses))
    return jsonify({'categories': categories})


if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5000, max_attempts=10):
        """Find a free port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return start_port  # Fallback to start_port if all attempts fail
    
    port = find_free_port(5000)
    
    if port != 5000:
        print(f"⚠️  Port 5000 is in use. Using port {port} instead.")
        print(f"   Access the app at: http://localhost:{port}")
        print()
    
    app.run(debug=True, host='0.0.0.0', port=port)

