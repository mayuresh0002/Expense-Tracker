#!/usr/bin/env python3
"""
Expense Tracker - Server Startup Script
Run this file to start the Flask web server
"""

import sys
import subprocess
import os

def check_flask():
    """Check if Flask is installed"""
    try:
        import flask
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Flask is not installed. Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies")
        return False

def main():
    """Main function to start the server"""
    print("=" * 50)
    print("  Expense Tracker - Web Server")
    print("=" * 50)
    print()
    
    # Check if Flask is installed
    if not check_flask():
        if not install_dependencies():
            sys.exit(1)
        print()
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("Error: app.py not found in current directory")
        sys.exit(1)
    
    print("Starting Flask server...")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Import and run the Flask app
    try:
        from app import app
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
            print(f"   (On macOS, port 5000 is often used by AirPlay Receiver)")
            print()
        
        print(f"✓ Server running at: http://localhost:{port}")
        print()
        
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

