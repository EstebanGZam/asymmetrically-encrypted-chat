# gui/__init__.py - GUI module initialization
"""
GUI module for Secure Chat System

This module provides a modern, elegant graphical user interface
for the asymmetrically encrypted chat system.

Components:
- MainWindow: Primary application window
- ChatWindow: Chat interface with encryption status
- ServerWindow: Server monitoring and logs
- styles: Modern dark theme and styling utilities
"""

__version__ = "1.0.0"
__author__ = "Secure Chat System"

# Import main components for easy access
from .main_window import MainWindow
from .chat_window import ChatWindow  
from .server_window import ServerWindow
from .styles import ModernTheme

__all__ = ['MainWindow', 'ChatWindow', 'ServerWindow', 'ModernTheme']