# gui/styles.py - Modern dark theme styles
import tkinter as tk
from tkinter import ttk

class ModernTheme:
    # Color palette
    DARK_BG = "#1e1e1e"
    DARKER_BG = "#161616"
    ACCENT = "#007acc"
    ACCENT_HOVER = "#005a9e"
    SUCCESS = "#16a085"
    WARNING = "#f39c12"
    ERROR = "#e74c3c"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_MUTED = "#6c6c6c"
    BORDER = "#404040"
    INPUT_BG = "#2d2d2d"
    CARD_BG = "#262626"
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure main frame style
        style.configure("Modern.TFrame", 
                       background=ModernTheme.DARK_BG,
                       borderwidth=0)
        
        # Configure card frame style
        style.configure("Card.TFrame",
                       background=ModernTheme.CARD_BG,
                       relief="flat",
                       borderwidth=1,
                       bordercolor=ModernTheme.BORDER)
        
        # Configure button styles
        style.configure("Modern.TButton",
                       background=ModernTheme.ACCENT,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       borderwidth=0,
                       focuscolor="none",
                       padding=(20, 10))
        
        style.map("Modern.TButton",
                 background=[("active", ModernTheme.ACCENT_HOVER),
                           ("pressed", ModernTheme.ACCENT_HOVER)])
        
        # Success button
        style.configure("Success.TButton",
                       background=ModernTheme.SUCCESS,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 8))
        
        # Entry style
        style.configure("Modern.TEntry",
                       fieldbackground=ModernTheme.INPUT_BG,
                       background=ModernTheme.INPUT_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       borderwidth=1,
                       insertcolor=ModernTheme.TEXT_PRIMARY,
                       selectbackground=ModernTheme.ACCENT)
        
        # Label styles
        style.configure("Title.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=("Segoe UI", 24, "bold"))
        
        style.configure("Subtitle.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.TEXT_SECONDARY,
                       font=("Segoe UI", 12))
        
        style.configure("Modern.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        
        style.configure("Card.TLabel",
                       background=ModernTheme.CARD_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        
        style.configure("Success.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.SUCCESS,
                       font=("Segoe UI", 10, "bold"))
        
        style.configure("Warning.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.WARNING,
                       font=("Segoe UI", 10, "bold"))
        
        style.configure("Error.TLabel",
                       background=ModernTheme.DARK_BG,
                       foreground=ModernTheme.ERROR,
                       font=("Segoe UI", 10, "bold"))

def create_rounded_button(parent, text, command, style_type="primary"):
    """Create a custom rounded button"""
    colors = {
        "primary": {"bg": ModernTheme.ACCENT, "hover": ModernTheme.ACCENT_HOVER},
        "success": {"bg": ModernTheme.SUCCESS, "hover": "#138d7a"},
        "warning": {"bg": ModernTheme.WARNING, "hover": "#e67e22"},
        "danger": {"bg": ModernTheme.ERROR, "hover": "#c0392b"}
    }
    
    color_set = colors.get(style_type, colors["primary"])
    
    btn = tk.Button(parent,
                   text=text,
                   command=command,
                   bg=color_set["bg"],
                   fg=ModernTheme.TEXT_PRIMARY,
                   font=("Segoe UI", 10, "bold"),
                   border=0,
                   relief="flat",
                   cursor="hand2",
                   padx=20,
                   pady=10)
    
    # Hover effects
    def on_enter(e):
        btn.config(bg=color_set["hover"])
    
    def on_leave(e):
        btn.config(bg=color_set["bg"])
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def create_modern_text(parent, **kwargs):
    """Create a modern styled text widget"""
    default_config = {
        "bg": ModernTheme.INPUT_BG,
        "fg": ModernTheme.TEXT_PRIMARY,
        "insertbackground": ModernTheme.TEXT_PRIMARY,
        "selectbackground": ModernTheme.ACCENT,
        "selectforeground": ModernTheme.TEXT_PRIMARY,
        "font": ("Consolas", 10),
        "border": 0,
        "relief": "flat",
        "wrap": tk.WORD
    }
    default_config.update(kwargs)
    
    return tk.Text(parent, **default_config)

def create_modern_entry(parent, placeholder="", **kwargs):
    """Create a modern styled entry widget with placeholder"""
    default_config = {
        "bg": ModernTheme.INPUT_BG,
        "fg": ModernTheme.TEXT_PRIMARY,
        "insertbackground": ModernTheme.TEXT_PRIMARY,
        "selectbackground": ModernTheme.ACCENT,
        "font": ("Segoe UI", 11),
        "border": 1,
        "relief": "solid",
        "bd": 1
    }
    default_config.update(kwargs)
    
    entry = tk.Entry(parent, **default_config)
    
    # Placeholder functionality
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=ModernTheme.TEXT_MUTED)
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=ModernTheme.TEXT_PRIMARY)
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=ModernTheme.TEXT_MUTED)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    return entry