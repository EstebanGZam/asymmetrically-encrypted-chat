# gui/main_window.py - Main application window
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from gui.styles import ModernTheme, create_rounded_button, create_modern_entry
from gui.server_window import ServerWindow
from gui.chat_window import ChatWindow
from gui_server import GUISecureChatServer

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Chat Seguro")
        self.root.geometry("500x600")
        self.root.configure(bg=ModernTheme.DARK_BG)
        self.root.resizable(True, True)
        
        # Configure styles
        ModernTheme.configure_styles()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        
        # Variables
        self.server_window = None
        self.chat_window = None
        self.server_instance = None
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        # App icon/title
        title_label = tk.Label(header_frame,
                              text="🔐",
                              font=("Segoe UI", 32),
                              bg=ModernTheme.DARK_BG,
                              fg=ModernTheme.ACCENT)
        title_label.pack()
        
        title_text = tk.Label(header_frame,
                             text="Chat Seguro",
                             font=("Segoe UI", 24, "bold"),
                             bg=ModernTheme.DARK_BG,
                             fg=ModernTheme.TEXT_PRIMARY)
        title_text.pack(pady=(5, 0))
        
        subtitle = tk.Label(header_frame,
                           text="Comunicación cifrada end-to-end con RSA 2048-bit",
                           font=("Segoe UI", 11),
                           bg=ModernTheme.DARK_BG,
                           fg=ModernTheme.TEXT_SECONDARY)
        subtitle.pack(pady=(5, 0))
    
    def create_main_content(self):
        """Create main content area"""
        # Main container
        main_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Server section
        self.create_server_section(main_frame)
        
        # Separator
        separator = tk.Frame(main_frame, height=2, bg=ModernTheme.BORDER)
        separator.pack(fill=tk.X, pady=30)
        
        # Client section
        self.create_client_section(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_server_section(self, parent):
        """Create server management section"""
        server_frame = tk.Frame(parent, bg=ModernTheme.CARD_BG, relief="flat", bd=1)
        server_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Inner padding
        inner_frame = tk.Frame(server_frame, bg=ModernTheme.CARD_BG)
        inner_frame.pack(fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        server_title = tk.Label(inner_frame,
                               text="🖥️ Servidor Relay",
                               font=("Segoe UI", 16, "bold"),
                               bg=ModernTheme.CARD_BG,
                               fg=ModernTheme.TEXT_PRIMARY)
        server_title.pack(anchor=tk.W)
        
        server_desc = tk.Label(inner_frame,
                              text="El servidor facilita el intercambio de llaves y retransmite mensajes cifrados",
                              font=("Segoe UI", 10),
                              bg=ModernTheme.CARD_BG,
                              fg=ModernTheme.TEXT_SECONDARY,
                              wraplength=400,
                              justify=tk.LEFT)
        server_desc.pack(anchor=tk.W, pady=(5, 15))
        
        # Server controls
        server_controls = tk.Frame(inner_frame, bg=ModernTheme.CARD_BG)
        server_controls.pack(fill=tk.X)
        
        self.server_btn = create_rounded_button(server_controls, 
                                               "🚀 Iniciar Servidor", 
                                               self.toggle_server,
                                               "success")
        self.server_btn.pack(side=tk.LEFT)
        
        self.server_status = tk.Label(server_controls,
                                     text="●",
                                     font=("Segoe UI", 16),
                                     bg=ModernTheme.CARD_BG,
                                     fg=ModernTheme.TEXT_MUTED)
        self.server_status.pack(side=tk.LEFT, padx=(15, 0))
        
        self.server_status_text = tk.Label(server_controls,
                                          text="Servidor desconectado",
                                          font=("Segoe UI", 10),
                                          bg=ModernTheme.CARD_BG,
                                          fg=ModernTheme.TEXT_MUTED)
        self.server_status_text.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_client_section(self, parent):
        """Create client connection section"""
        client_frame = tk.Frame(parent, bg=ModernTheme.CARD_BG, relief="flat", bd=1)
        client_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Inner padding
        inner_frame = tk.Frame(client_frame, bg=ModernTheme.CARD_BG)
        inner_frame.pack(fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        client_title = tk.Label(inner_frame,
                               text="💬 Cliente de Chat",
                               font=("Segoe UI", 16, "bold"),
                               bg=ModernTheme.CARD_BG,
                               fg=ModernTheme.TEXT_PRIMARY)
        client_title.pack(anchor=tk.W)
        
        client_desc = tk.Label(inner_frame,
                              text="Conecta como cliente para participar en conversaciones seguras",
                              font=("Segoe UI", 10),
                              bg=ModernTheme.CARD_BG,
                              fg=ModernTheme.TEXT_SECONDARY,
                              wraplength=400,
                              justify=tk.LEFT)
        client_desc.pack(anchor=tk.W, pady=(5, 15))
        
        # Username input
        input_frame = tk.Frame(inner_frame, bg=ModernTheme.CARD_BG)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        username_label = tk.Label(input_frame,
                                 text="Nombre de usuario:",
                                 font=("Segoe UI", 10, "bold"),
                                 bg=ModernTheme.CARD_BG,
                                 fg=ModernTheme.TEXT_PRIMARY)
        username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = create_modern_entry(input_frame, 
                                                 placeholder="Ingresa tu nombre de usuario")
        self.username_entry.pack(fill=tk.X, ipady=8)
        
        # Connect button
        connect_btn = create_rounded_button(inner_frame,
                                           "🔗 Conectar como Cliente",
                                           self.connect_client,
                                           "primary")
        connect_btn.pack(pady=(10, 0))
    
    def create_footer(self, parent):
        """Create application footer"""
        footer_frame = tk.Frame(parent, bg=ModernTheme.DARK_BG)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        
        # Security info
        security_info = tk.Label(footer_frame,
                                text="🔒 Cifrado RSA 2048-bit • 🔑 Intercambio seguro de llaves • ✅ Firmas digitales",
                                font=("Segoe UI", 9),
                                bg=ModernTheme.DARK_BG,
                                fg=ModernTheme.TEXT_MUTED)
        security_info.pack()
    
    def toggle_server(self):
        """Toggle server on/off"""
        if self.server_instance is None:
            self.start_server()
        else:
            self.stop_server()
    
    def start_server(self):
        """Start the relay server"""
        try:
            # Create server instance
            self.server_instance = GUISecureChatServer()
            
            # Start server in separate thread
            server_thread = threading.Thread(target=self.server_instance.start, daemon=True)
            server_thread.start()
            
            # Update UI
            self.server_btn.config(text="🛑 Detener Servidor")
            self.server_status.config(fg=ModernTheme.SUCCESS)
            self.server_status_text.config(text="Servidor activo en localhost:8888", 
                                          fg=ModernTheme.SUCCESS)
            
            # Show server window
            self.server_window = ServerWindow(self.root, self.server_instance)
            
            messagebox.showinfo("Servidor", "¡Servidor iniciado correctamente!\nDisponible en localhost:8888")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor:\n{e}")
            self.server_instance = None
    
    def stop_server(self):
        """Stop the relay server"""
        if self.server_instance:
            self.server_instance.stop()
            self.server_instance = None
            
            # Close server window
            if self.server_window:
                self.server_window.close()
                self.server_window = None
            
            # Update UI
            self.server_btn.config(text="🚀 Iniciar Servidor")
            self.server_status.config(fg=ModernTheme.TEXT_MUTED)
            self.server_status_text.config(text="Servidor desconectado", 
                                          fg=ModernTheme.TEXT_MUTED)
            
            messagebox.showinfo("Servidor", "Servidor detenido correctamente")
    
    def connect_client(self):
        """Connect as client"""
        username = self.username_entry.get().strip()
        
        # Remove placeholder text
        if username == "Ingresa tu nombre de usuario" or not username:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido")
            return
        
        try:
            # Create and show chat window
            self.chat_window = ChatWindow(username, parent=self.root)
            self.chat_window.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar como cliente:\n{e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if self.server_instance:
            self.server_instance.stop()
        self.root.destroy()