# gui/server_window.py - Server monitoring window
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from gui.styles import ModernTheme, create_rounded_button

class ServerWindow:
    def __init__(self, parent, server_instance):
        self.parent = parent
        self.server = server_instance
        self.root = tk.Toplevel(parent)
        self.root.title("Monitor del Servidor")
        self.root.geometry("600x500")
        self.root.configure(bg=ModernTheme.DARK_BG)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure styles
        ModernTheme.configure_styles()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_interface()
        
        # Set callback for server events
        if hasattr(server_instance, 'set_gui_callback'):
            server_instance.set_gui_callback(self.handle_server_event)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Create server monitoring interface"""
        # Header
        self.create_header()
        
        # Status section
        self.create_status_section()
        
        # Logs section
        self.create_logs_section()
        
        # Controls section
        self.create_controls_section()
    
    def create_header(self):
        """Create window header"""
        header_frame = tk.Frame(self.root, bg=ModernTheme.CARD_BG, height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Inner frame
        inner_header = tk.Frame(header_frame, bg=ModernTheme.CARD_BG)
        inner_header.pack(fill=tk.BOTH, padx=20, pady=15)
        
        # Server icon and title
        server_icon = tk.Label(inner_header,
                              text="🖥️",
                              font=("Segoe UI", 24),
                              bg=ModernTheme.CARD_BG,
                              fg=ModernTheme.ACCENT)
        server_icon.pack(side=tk.LEFT)
        
        title_frame = tk.Frame(inner_header, bg=ModernTheme.CARD_BG)
        title_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 0))
        
        title_label = tk.Label(title_frame,
                              text="Servidor Relay",
                              font=("Segoe UI", 16, "bold"),
                              bg=ModernTheme.CARD_BG,
                              fg=ModernTheme.TEXT_PRIMARY)
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Monitor de actividad y conexiones",
                                 font=("Segoe UI", 10),
                                 bg=ModernTheme.CARD_BG,
                                 fg=ModernTheme.TEXT_SECONDARY)
        subtitle_label.pack(anchor=tk.W)
        
        # Status indicator
        self.server_status = tk.Label(inner_header,
                                     text="● ACTIVO",
                                     font=("Segoe UI", 12, "bold"),
                                     bg=ModernTheme.CARD_BG,
                                     fg=ModernTheme.SUCCESS)
        self.server_status.pack(side=tk.RIGHT)
    
    def create_status_section(self):
        """Create server status section"""
        status_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        # Title
        status_title = tk.Label(status_frame,
                               text="📊 Estado del Servidor",
                               font=("Segoe UI", 12, "bold"),
                               bg=ModernTheme.DARK_BG,
                               fg=ModernTheme.TEXT_PRIMARY)
        status_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Status cards container
        cards_frame = tk.Frame(status_frame, bg=ModernTheme.DARK_BG)
        cards_frame.pack(fill=tk.X)
        
        # Connected clients card
        clients_card = tk.Frame(cards_frame, bg=ModernTheme.CARD_BG, relief="flat", bd=1)
        clients_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        clients_inner = tk.Frame(clients_card, bg=ModernTheme.CARD_BG)
        clients_inner.pack(fill=tk.BOTH, padx=15, pady=15)
        
        clients_label = tk.Label(clients_inner,
                                text="👥 Clientes Conectados",
                                font=("Segoe UI", 10, "bold"),
                                bg=ModernTheme.CARD_BG,
                                fg=ModernTheme.TEXT_PRIMARY)
        clients_label.pack()
        
        self.clients_count = tk.Label(clients_inner,
                                     text="0",
                                     font=("Segoe UI", 20, "bold"),
                                     bg=ModernTheme.CARD_BG,
                                     fg=ModernTheme.ACCENT)
        self.clients_count.pack()
        
        # Messages relayed card
        messages_card = tk.Frame(cards_frame, bg=ModernTheme.CARD_BG, relief="flat", bd=1)
        messages_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        messages_inner = tk.Frame(messages_card, bg=ModernTheme.CARD_BG)
        messages_inner.pack(fill=tk.BOTH, padx=15, pady=15)
        
        messages_label = tk.Label(messages_inner,
                                 text="📨 Mensajes Relay",
                                 font=("Segoe UI", 10, "bold"),
                                 bg=ModernTheme.CARD_BG,
                                 fg=ModernTheme.TEXT_PRIMARY)
        messages_label.pack()
        
        self.messages_count = tk.Label(messages_inner,
                                      text="0",
                                      font=("Segoe UI", 20, "bold"),
                                      bg=ModernTheme.CARD_BG,
                                      fg=ModernTheme.SUCCESS)
        self.messages_count.pack()
    
    def create_logs_section(self):
        """Create logs display section"""
        logs_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))
        
        # Title
        logs_title = tk.Label(logs_frame,
                             text="📝 Registro de Actividad",
                             font=("Segoe UI", 12, "bold"),
                             bg=ModernTheme.DARK_BG,
                             fg=ModernTheme.TEXT_PRIMARY)
        logs_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            bg=ModernTheme.INPUT_BG,
            fg=ModernTheme.TEXT_PRIMARY,
            font=("Consolas", 9),
            border=0,
            relief="flat",
            wrap=tk.WORD,
            state=tk.DISABLED,
            selectbackground=ModernTheme.ACCENT,
            insertbackground=ModernTheme.TEXT_PRIMARY
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different log levels
        self.logs_text.tag_configure("info", foreground=ModernTheme.TEXT_PRIMARY)
        self.logs_text.tag_configure("success", foreground=ModernTheme.SUCCESS)
        self.logs_text.tag_configure("warning", foreground=ModernTheme.WARNING)
        self.logs_text.tag_configure("error", foreground=ModernTheme.ERROR)
        self.logs_text.tag_configure("system", foreground=ModernTheme.TEXT_SECONDARY)
        
        # Initial log
        self.add_log("🚀 Servidor iniciado en localhost:8888", "success")
        self.add_log("💡 El servidor NO puede leer mensajes - solo actúa como relay", "info")
        self.add_log("🔄 Esperando conexiones de clientes...", "info")
    
    def create_controls_section(self):
        """Create controls section"""
        controls_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        controls_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Clear logs button
        clear_btn = create_rounded_button(controls_frame,
                                         "🗑️ Limpiar Logs",
                                         self.clear_logs,
                                         "warning")
        clear_btn.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = create_rounded_button(controls_frame,
                                           "🔄 Actualizar",
                                           self.refresh_status,
                                           "primary")
        refresh_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    def handle_server_event(self, event_type, data):
        """Handle events from server"""
        self.root.after(0, lambda: self._handle_server_event_ui(event_type, data))
    
    def _handle_server_event_ui(self, event_type, data):
        """Handle server events in UI thread"""
        if event_type == "client_connected":
            username = data.get("username", "Desconocido")
            address = data.get("address", "")
            self.add_log(f"✅ Cliente conectado: {username} desde {address}", "success")
            self.update_client_count(data.get("total_clients", 0))
            
        elif event_type == "client_disconnected":
            username = data.get("username", "Desconocido")
            self.add_log(f"🔌 Cliente desconectado: {username}", "warning")
            self.update_client_count(data.get("total_clients", 0))
            
        elif event_type == "key_exchange":
            user1 = data.get("user1", "Usuario1")
            user2 = data.get("user2", "Usuario2")
            self.add_log(f"🔑 Intercambio de llaves: {user1} ↔ {user2}", "info")
            
        elif event_type == "message_relay":
            sender = data.get("sender", "Desconocido")
            receiver = data.get("receiver", "Desconocido")
            self.add_log(f"📨 Mensaje relay: {sender} → {receiver} (ENCRIPTADO)", "info")
            self.increment_messages_count()
            
        elif event_type == "error":
            error_msg = data.get("message", "Error desconocido")
            self.add_log(f"❌ Error: {error_msg}", "error")
    
    def add_log(self, message, level="info"):
        """Add a log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.insert(tk.END, full_message, level)
        self.logs_text.see(tk.END)
        self.logs_text.config(state=tk.DISABLED)
    
    def update_client_count(self, count):
        """Update connected clients count"""
        self.clients_count.config(text=str(count))
        
        # Update color based on count
        if count == 0:
            self.clients_count.config(fg=ModernTheme.TEXT_MUTED)
        elif count == 1:
            self.clients_count.config(fg=ModernTheme.WARNING)
        else:
            self.clients_count.config(fg=ModernTheme.SUCCESS)
    
    def increment_messages_count(self):
        """Increment messages relayed count"""
        try:
            current = int(self.messages_count.cget("text"))
            self.messages_count.config(text=str(current + 1))
        except:
            self.messages_count.config(text="1")
    
    def clear_logs(self):
        """Clear the logs display"""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        self.logs_text.config(state=tk.DISABLED)
        
        # Add cleared message
        self.add_log("🗑️ Logs limpiados", "system")
    
    def refresh_status(self):
        """Refresh server status"""
        # This would typically query the server for current status
        self.add_log("🔄 Estado actualizado", "info")
    
    def close(self):
        """Close the server window"""
        if self.root:
            self.root.destroy()
    
    def on_closing(self):
        """Handle window closing"""
        self.close()