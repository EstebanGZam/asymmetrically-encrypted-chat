# main_gui.py - GUI entry point for Secure Chat System
import sys
import tkinter as tk
from tkinter import messagebox
import os

# Add gui directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gui'))

from gui.main_window import MainWindow

def main():
    """Main entry point for GUI application"""
    try:
        # Create and run main window
        app = MainWindow()
        
        # Set up proper closing behavior
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Run the application
        app.run()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", 
                           f"Error iniciando la aplicación:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()