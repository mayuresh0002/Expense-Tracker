# Running Expense Tracker on macOS

This guide will help you run the Expense Tracker application on your Mac.

## Prerequisites

1. **Check if Python 3 is installed:**
   Open Terminal (Applications → Utilities → Terminal) and run:
   ```bash
   python3 --version
   ```
   
   If Python is not installed, install it using Homebrew:
   ```bash
   brew install python3
   ```
   Or download from [python.org](https://www.python.org/downloads/)

2. **Check if pip is installed:**
   ```bash
   pip3 --version
   ```

## Step-by-Step Setup

### Step 1: Open Terminal

1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal" and press Enter
3. Or go to Applications → Utilities → Terminal

### Step 2: Navigate to Project Directory

In Terminal, navigate to the project folder:
```bash
cd ~/Desktop/CSE
```

### Step 3: Install Dependencies

Install Flask and other required packages:
```bash
pip3 install -r requirements.txt
```

If you get a permission error, use:
```bash
pip3 install --user -r requirements.txt
```

### Step 4: Run the Server

You have three options:

#### Option A: Using the Python Script (Easiest)
```bash
python3 run_server.py
```

#### Option B: Using the Shell Script
```bash
./run_server.sh
```

If you get a "permission denied" error, make it executable first:
```bash
chmod +x run_server.sh
./run_server.sh
```

#### Option C: Direct Flask Command
```bash
python3 app.py
```

### Step 5: Open in Browser

Once the server starts, you'll see:
```
Starting Flask server...
Server will be available at: http://localhost:5000
```

1. Open Safari, Chrome, or any web browser
2. Go to: `http://localhost:5000`
3. You should see the Expense Tracker interface!

### Step 6: Stop the Server

To stop the server, press `Ctrl + C` in the Terminal window.

## Quick Start (All-in-One)

Copy and paste these commands one by one in Terminal:

```bash
# Navigate to project
cd ~/Desktop/CSE

# Install dependencies
pip3 install -r requirements.txt

# Run the server
python3 run_server.py
```

Then check the terminal output for the server URL (it will show the port number, which may be 5000, 5001, etc. depending on availability).

## Troubleshooting

### Issue: "python3: command not found"
**Solution:** Install Python 3 from [python.org](https://www.python.org/downloads/) or using Homebrew:
```bash
brew install python3
```

### Issue: "pip3: command not found"
**Solution:** Python 3 should include pip3. If not, install it:
```bash
python3 -m ensurepip --upgrade
```

### Issue: "Permission denied" when running shell script
**Solution:** Make the script executable:
```bash
chmod +x run_server.sh
```

### Issue: "Port 5000 already in use"
**Solution:** This is a common issue on macOS where AirPlay Receiver uses port 5000. 

**Automatic Fix (Recommended):** The app now automatically detects if port 5000 is in use and will use the next available port (5001, 5002, etc.). Just look at the terminal output to see which port it's using, then open that URL in your browser.

**Manual Fix (Optional):** If you want to use port 5000 specifically, you can disable AirPlay Receiver:
1. Open **System Preferences** (or **System Settings** on newer macOS)
2. Go to **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**

Or you can manually specify a different port by modifying `app.py` (change `port=5000` to `port=5001`).

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask:
```bash
pip3 install Flask
```

Or reinstall all dependencies:
```bash
pip3 install -r requirements.txt
```

## Running the CLI Version

If you prefer the command-line interface instead of the web version:

```bash
cd ~/Desktop/CSE
python3 expense_tracker.py
```

## Tips

- Keep the Terminal window open while using the web application
- The server runs in the foreground - you'll see logs in the Terminal
- Data is saved automatically to `expenses.json` in the project folder
- You can run the server anytime by repeating Step 4

## Need Help?

If you encounter any issues:
1. Make sure you're in the correct directory (`~/Desktop/CSE`)
2. Verify Python 3 is installed: `python3 --version`
3. Check that all dependencies are installed: `pip3 list | grep Flask`
4. Try running with verbose output: `python3 -v run_server.py`

