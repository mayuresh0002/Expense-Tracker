# Expense Tracker

A simple expense tracking application built with Python, available as both a command-line tool and a modern web application.

## Features

- ✅ Add expenses with description, amount, category, and date
- 📊 View all expenses in a formatted table
- 🔍 Filter expenses by category or month
- 🗑️ Delete expenses by ID
- 📈 View statistics (total, average, breakdown by category)
- 📁 Automatic data persistence (saves to JSON file)
- 🏷️ List all expense categories
- 🌐 Beautiful web interface with modern UI

## Requirements

- Python 3.6 or higher
- Flask (for web version only)

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed on your system
3. Install dependencies:

```bash
pip install -r requirements.txt
```

**📱 macOS Users:** See [MACOS_SETUP.md](MACOS_SETUP.md) for detailed macOS-specific instructions.

## Usage

### Web Application (Recommended)

Run the Flask web server using one of these methods:

**Option 1: Using the run server script (Recommended)**
```bash
python run_server.py
```

**Option 2: Using the shell script**
```bash
./run_server.sh
```

**Option 3: Direct Flask command**
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The run server scripts will automatically check for dependencies and install them if needed.

The web interface provides:
- Modern, responsive design
- Real-time updates
- Interactive forms and filters
- Visual statistics and category breakdowns
- Easy expense management

### Command-Line Interface

Run the expense tracker:

```bash
python expense_tracker.py
```

### Menu Options

1. **Add Expense** - Add a new expense entry
   - Enter description, amount, category, and optionally a date
   - If no date is provided, today's date is used

2. **View All Expenses** - Display all expenses in a formatted table

3. **View Expenses by Category** - Filter and view expenses for a specific category

4. **View Expenses by Month** - Filter expenses by month (format: YYYY-MM)

5. **Delete Expense** - Remove an expense by entering its ID

6. **View Statistics** - See total expenses, average, and breakdown by category

7. **List Categories** - Display all unique expense categories

8. **Exit** - Quit the application

## Data Storage

Expenses are automatically saved to `expenses.json` in the same directory as the script. The data persists between sessions.

## Example Usage

```
EXPENSE TRACKER
==================================================
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. View Expenses by Month (YYYY-MM)
5. Delete Expense
6. View Statistics
7. List Categories
8. Exit
==================================================

Enter your choice (1-8): 1

--- Add New Expense ---
Description: Groceries
Amount: ₹45.50
Category: Food
Date (YYYY-MM-DD, press Enter for today): 

✓ Expense added successfully!
```

## File Structure

```
CSE/
├── app.py                    # Flask web application
├── expense_tracker.py        # Core expense tracker module (CLI)
├── run_server.py            # Python script to start the server
├── run_server.sh            # Shell script to start the server
├── expenses.json             # Data file (created automatically)
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface HTML
├── static/
│   ├── style.css           # CSS styling
│   └── script.js           # JavaScript for interactions
└── README.md                # This file
```

## License

This project is open source and available for personal use.

