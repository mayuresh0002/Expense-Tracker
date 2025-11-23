#!/usr/bin/env python3
"""
Expense Tracker - A simple command-line expense tracking application
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Expense:
    """Represents a single expense entry"""
    
    def __init__(self, description: str, amount: float, category: str, date: Optional[str] = None):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def to_dict(self) -> Dict:
        """Convert expense to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        """Create expense from dictionary"""
        expense = cls(
            description=data['description'],
            amount=data['amount'],
            category=data['category'],
            date=data['date']
        )
        expense.id = data['id']
        return expense
    
    def __str__(self) -> str:
        return f"{self.date} | {self.category:15} | ₹{self.amount:10.2f} | {self.description}"


class ExpenseTracker:
    """Main expense tracker class"""
    
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self.expenses: List[Expense] = []
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = [Expense.from_dict(exp) for exp in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading expenses: {e}")
                self.expenses = []
        else:
            self.expenses = []
    
    def save_expenses(self):
        """Save expenses to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                data = [exp.to_dict() for exp in self.expenses]
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving expenses: {e}")
            return False
    
    def add_expense(self, description: str, amount: float, category: str, date: Optional[str] = None):
        """Add a new expense"""
        if amount <= 0:
            print("Error: Amount must be greater than 0")
            return False
        
        expense = Expense(description, amount, category, date)
        self.expenses.append(expense)
        if self.save_expenses():
            print(f"✓ Expense added successfully!")
            return True
        return False
    
    def view_expenses(self, category: Optional[str] = None, month: Optional[str] = None):
        """View all expenses, optionally filtered by category or month"""
        filtered_expenses = self.expenses
        
        if category:
            filtered_expenses = [e for e in filtered_expenses if e.category.lower() == category.lower()]
        
        if month:
            filtered_expenses = [e for e in filtered_expenses if e.date.startswith(month)]
        
        if not filtered_expenses:
            print("No expenses found.")
            return
        
        # Sort by date (newest first)
        filtered_expenses.sort(key=lambda x: x.date, reverse=True)
        
        print("\n" + "="*80)
        print(f"{'Date':<12} {'Category':<15} {'Amount':<12} {'Description'}")
        print("="*80)
        
        total = 0
        for expense in filtered_expenses:
            print(expense)
            total += expense.amount
        
        print("="*80)
        print(f"{'Total':<28} ₹{total:>10.2f}")
        print("="*80 + "\n")
    
    def delete_expense(self, expense_id: str):
        """Delete an expense by ID"""
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        
        if len(self.expenses) < original_count:
            if self.save_expenses():
                print("✓ Expense deleted successfully!")
                return True
        else:
            print("Error: Expense not found.")
            return False
    
    def get_statistics(self):
        """Get expense statistics"""
        if not self.expenses:
            print("No expenses to analyze.")
            return
        
        total = sum(e.amount for e in self.expenses)
        category_totals = {}
        
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        
        print("\n" + "="*50)
        print("EXPENSE STATISTICS")
        print("="*50)
        print(f"Total Expenses: ₹{total:.2f}")
        print(f"Number of Transactions: {len(self.expenses)}")
        print(f"Average per Transaction: ₹{total/len(self.expenses):.2f}")
        print("\nBy Category:")
        print("-"*50)
        
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            print(f"{category:20} ₹{amount:>10.2f} ({percentage:>5.1f}%)")
        
        print("="*50 + "\n")
    
    def list_categories(self):
        """List all unique categories"""
        categories = sorted(set(e.category for e in self.expenses))
        if categories:
            print("\nCategories:")
            for cat in categories:
                print(f"  - {cat}")
        else:
            print("No categories found.")
        print()


def main():
    """Main CLI interface"""
    tracker = ExpenseTracker()
    
    while True:
        print("\n" + "="*50)
        print("EXPENSE TRACKER")
        print("="*50)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. View Expenses by Month (YYYY-MM)")
        print("5. Delete Expense")
        print("6. View Statistics")
        print("7. List Categories")
        print("8. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n--- Add New Expense ---")
            description = input("Description: ").strip()
            if not description:
                print("Error: Description cannot be empty")
                continue
            
            try:
                amount = float(input("Amount: ₹").strip())
            except ValueError:
                print("Error: Invalid amount")
                continue
            
            category = input("Category: ").strip()
            if not category:
                print("Error: Category cannot be empty")
                continue
            
            date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
            date = date_input if date_input else None
            
            tracker.add_expense(description, amount, category, date)
        
        elif choice == '2':
            tracker.view_expenses()
        
        elif choice == '3':
            category = input("Enter category: ").strip()
            tracker.view_expenses(category=category)
        
        elif choice == '4':
            month = input("Enter month (YYYY-MM): ").strip()
            tracker.view_expenses(month=month)
        
        elif choice == '5':
            print("\n--- Delete Expense ---")
            tracker.view_expenses()
            expense_id = input("Enter expense ID to delete: ").strip()
            if expense_id:
                tracker.delete_expense(expense_id)
        
        elif choice == '6':
            tracker.get_statistics()
        
        elif choice == '7':
            tracker.list_categories()
        
        elif choice == '8':
            print("\nThank you for using Expense Tracker!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

