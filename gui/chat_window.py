# gui/chat_window.py - Modern chat interface
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import threading
from gui.styles import ModernTheme, create_rounded_button, create_modern_entry
from gui_client import GUISecureChatClient

class ChatWindow:
    def __init__(self, username, parent=None):
        self.username = username
        self.parent = parent
        self.client = None
        self.root = None
        self.peer_verified = False
        self.is_closing = False
        
    def show(self):
        """Show chat window"""
        self.root = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.root.title(f"Chat Seguro - {self.username}")
        self.root.geometry("800x600")
        self.root.configure(bg=ModernTheme.DARK_BG)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure styles
        ModernTheme.configure_styles()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_chat_interface()
        
        # Initialize client
        self.init_client()
        
        # Start connection
        self.connect_to_server()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_chat_interface(self):
        """Create the chat interface"""
        # Header
        self.create_header()
        
        # Main chat area
        self.create_chat_area()
        
        # Security status
        self.create_security_status()
        
        # Input area
        self.create_input_area()
    
    def create_header(self):
        """Create chat header"""
        header_frame = tk.Frame(self.root, bg=ModernTheme.CARD_BG, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Inner frame for content
        inner_header = tk.Frame(header_frame, bg=ModernTheme.CARD_BG)
        inner_header.pack(fill=tk.BOTH, padx=20, pady=15)
        
        # Left side - user info
        left_frame = tk.Frame(inner_header, bg=ModernTheme.CARD_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        user_icon = tk.Label(left_frame,
                            text="👤",
                            font=("Segoe UI", 20),
                            bg=ModernTheme.CARD_BG,
                            fg=ModernTheme.ACCENT)
        user_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        user_info_frame = tk.Frame(left_frame, bg=ModernTheme.CARD_BG)
        user_info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        user_label = tk.Label(user_info_frame,
                             text=f"Conectado como: {self.username}",
                             font=("Segoe UI", 12, "bold"),
                             bg=ModernTheme.CARD_BG,
                             fg=ModernTheme.TEXT_PRIMARY)
        user_label.pack(anchor=tk.W)
        
        self.status_label = tk.Label(user_info_frame,
                                    text="🔄 Conectando...",
                                    font=("Segoe UI", 10),
                                    bg=ModernTheme.CARD_BG,
                                    fg=ModernTheme.WARNING)
        self.status_label.pack(anchor=tk.W)
        
        # Right side - connection status
        right_frame = tk.Frame(inner_header, bg=ModernTheme.CARD_BG)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.connection_status = tk.Label(right_frame,
                                         text="●",
                                         font=("Segoe UI", 16),
                                         bg=ModernTheme.CARD_BG,
                                         fg=ModernTheme.WARNING)
        self.connection_status.pack(side=tk.RIGHT)
    
    def create_chat_area(self):
        """Create main chat messages area"""
        chat_container = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))
        
        # Messages frame with scrollbar
        messages_frame = tk.Frame(chat_container, bg=ModernTheme.DARK_BG)
        messages_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrolled text widget for messages
        self.messages_text = scrolledtext.ScrolledText(
            messages_frame,
            bg=ModernTheme.INPUT_BG,
            fg=ModernTheme.TEXT_PRIMARY,
            font=("Consolas", 10),
            border=0,
            relief="flat",
            wrap=tk.WORD,
            state=tk.DISABLED,
            selectbackground=ModernTheme.ACCENT,
            insertbackground=ModernTheme.TEXT_PRIMARY
        )
        self.messages_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Configure text tags for different message types
        self.messages_text.tag_configure("system", foreground=ModernTheme.TEXT_SECONDARY)
        self.messages_text.tag_configure("own", foreground=ModernTheme.ACCENT, font=("Consolas", 10, "bold"))
        self.messages_text.tag_configure("peer", foreground=ModernTheme.SUCCESS, font=("Consolas", 10, "bold"))
        self.messages_text.tag_configure("warning", foreground=ModernTheme.WARNING)
        self.messages_text.tag_configure("error", foreground=ModernTheme.ERROR)
        self.messages_text.tag_configure("success", foreground=ModernTheme.SUCCESS)
        
        # Welcome message
        self.add_system_message("🔐 Sistema de Chat Seguro iniciado")
        self.add_system_message("⚡ Generando par de llaves RSA 2048-bit...")
    
    def create_security_status(self):
        """Create security status bar"""
        self.security_frame = tk.Frame(self.root, bg=ModernTheme.CARD_BG, height=60)
        self.security_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        self.security_frame.pack_propagate(False)
        
        # Inner frame
        inner_security = tk.Frame(self.security_frame, bg=ModernTheme.CARD_BG)
        inner_security.pack(fill=tk.BOTH, padx=15, pady=10)
        
        # Security status
        self.security_icon = tk.Label(inner_security,
                                     text="🔒",
                                     font=("Segoe UI", 16),
                                     bg=ModernTheme.CARD_BG,
                                     fg=ModernTheme.TEXT_MUTED)
        self.security_icon.pack(side=tk.LEFT)
        
        self.security_text = tk.Label(inner_security,
                                     text="Esperando intercambio de llaves...",
                                     font=("Segoe UI", 10),
                                     bg=ModernTheme.CARD_BG,
                                     fg=ModernTheme.TEXT_MUTED)
        self.security_text.pack(side=tk.LEFT, padx=(10, 0))
        
        # Verify button (initially hidden)
        self.verify_btn = create_rounded_button(inner_security,
                                               "✅ Verificar Identidad",
                                               self.verify_peer,
                                               "success")
        self.verify_btn.pack(side=tk.RIGHT)
        self.verify_btn.pack_forget()  # Hide initially
    
    def create_input_area(self):
        """Create message input area"""
        input_frame = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        input_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # Input container
        input_container = tk.Frame(input_frame, bg=ModernTheme.INPUT_BG, relief="flat", bd=1)
        input_container.pack(fill=tk.X)
        
        # Message entry
        self.message_entry = tk.Entry(input_container,
                                     bg=ModernTheme.INPUT_BG,
                                     fg=ModernTheme.TEXT_PRIMARY,
                                     font=("Segoe UI", 11),
                                     border=0,
                                     relief="flat",
                                     insertbackground=ModernTheme.TEXT_PRIMARY,
                                     selectbackground=ModernTheme.ACCENT)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=12)
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.bind("<KeyPress>", self.on_typing)
        
        # Send button
        send_btn = create_rounded_button(input_container,
                                        "Enviar",
                                        self.send_message,
                                        "primary")
        send_btn.pack(side=tk.RIGHT, padx=(0, 15))
        
        # Initially disable input
        self.message_entry.config(state=tk.DISABLED)
    
    def init_client(self):
        """Initialize the secure chat client"""
        self.client = GUISecureChatClient(
            username=self.username,
            gui_callback=self.handle_client_message
        )
    
    def connect_to_server(self):
        """Connect to server in background thread"""
        def connect():
            try:
                success = self.client.connect()
                if success:
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, self.on_connection_failed)
            except Exception as e:
                self.root.after(0, lambda: self.on_connection_failed(str(e)))
        
        threading.Thread(target=connect, daemon=True).start()
    
    def on_connection_success(self):
        """Handle successful connection"""
        self.status_label.config(text="✅ Conectado", fg=ModernTheme.SUCCESS)
        self.connection_status.config(fg=ModernTheme.SUCCESS)
        self.add_system_message("✅ Conectado al servidor relay")
        self.add_system_message("🔄 Esperando otro usuario para iniciar intercambio de llaves...")
    
    def on_connection_failed(self, error=None):
        """Handle connection failure"""
        self.status_label.config(text="❌ Error de conexión", fg=ModernTheme.ERROR)
        self.connection_status.config(fg=ModernTheme.ERROR)
        error_msg = f"❌ Error de conexión: {error}" if error else "❌ No se pudo conectar al servidor"
        self.add_system_message(error_msg)
        messagebox.showerror("Error de Conexión", 
                           "No se pudo conectar al servidor.\nAsegúrate de que el servidor esté ejecutándose.")
    
    def handle_client_message(self, msg_type, data):
        """Handle messages from client"""
        self.root.after(0, lambda: self._handle_client_message_ui(msg_type, data))
    
    def _handle_client_message_ui(self, msg_type, data):
        """Handle client messages in UI thread"""
        if self.is_closing:
            return
            
        if msg_type == "key_exchange":
            self.on_key_exchange(data)
        elif msg_type == "message":
            self.on_message_received(data)
        elif msg_type == "error":
            self.on_error(data)
        elif msg_type == "status":
            self.on_status_update(data)
    
    def on_key_exchange(self, data):
        """Handle key exchange completion"""
        peer_name = data.get("peer_name", "Usuario")
        fingerprint = data.get("fingerprint", "")
        
        self.add_system_message(f"🔑 Intercambio de llaves con {peer_name} completado")
        self.add_system_message(f"🔍 Fingerprint de {peer_name}:")
        self.add_system_message(f"    {fingerprint}")
        self.add_system_message("⚠️  IMPORTANTE: Verifica este fingerprint por un canal seguro!")
        
        # Update security status
        self.security_text.config(text=f"Llaves intercambiadas con {peer_name} - SIN VERIFICAR",
                                 fg=ModernTheme.WARNING)
        self.security_icon.config(text="⚠️", fg=ModernTheme.WARNING)
        
        # Show verify button
        self.verify_btn.pack(side=tk.RIGHT)
        
        # Enable message input
        self.message_entry.config(state=tk.NORMAL)
        self.message_entry.focus()
        
        self.status_label.config(text="⚠️  Sin verificar", fg=ModernTheme.WARNING)
    
    def on_message_received(self, data):
        """Handle received message"""
        sender = data.get("sender", "Desconocido")
        message = data.get("message", "")
        timestamp = data.get("timestamp", datetime.now())
        signature_valid = data.get("signature_valid", False)
        
        # Format timestamp
        time_str = timestamp.strftime("%H:%M:%S")
        
        # Add message with appropriate styling
        signature_indicator = "✅" if signature_valid else "❌"
        full_message = f"[{time_str}] {signature_indicator} {sender}: {message}\n"
        
        self.add_message(full_message, "peer" if signature_valid else "error")
        
        if not signature_valid:
            self.add_system_message("⚠️  ADVERTENCIA: Firma digital inválida!")
    
    def on_error(self, error_msg):
        """Handle error messages"""
        self.add_system_message(f"❌ Error: {error_msg}")
    
    def on_status_update(self, status):
        """Handle status updates"""
        self.add_system_message(f"ℹ️  {status}")
    
    def verify_peer(self):
        """Mark peer as verified"""
        self.peer_verified = True
        
        # Update security status
        self.security_text.config(text="✅ Identidad verificada - Canal seguro establecido",
                                 fg=ModernTheme.SUCCESS)
        self.security_icon.config(text="🔒", fg=ModernTheme.SUCCESS)
        self.status_label.config(text="🔒 Canal seguro", fg=ModernTheme.SUCCESS)
        
        # Hide verify button
        self.verify_btn.pack_forget()
        
        self.add_system_message("✅ Identidad verificada - Canal seguro establecido")
        self.add_system_message("💬 Ya puedes enviar mensajes de forma segura")
    
    def send_message(self, event=None):
        """Send a message"""
        if not self.client or not self.client.connected:
            return
            
        message = self.message_entry.get().strip()
        if not message:
            return
        
        try:
            # Send through client
            success = self.client.send_message(message)
            
            if success:
                # Add to chat display
                timestamp = datetime.now().strftime("%H:%M:%S")
                verification_status = "✅" if self.peer_verified else "⚠️"
                full_message = f"[{timestamp}] {verification_status} Tú: {message}\n"
                self.add_message(full_message, "own")
                
                if not self.peer_verified:
                    self.add_system_message("⚠️  Mensaje enviado sin verificar identidad del destinatario")
                
                # Clear input
                self.message_entry.delete(0, tk.END)
            else:
                self.add_system_message("❌ Error enviando mensaje")
                
        except Exception as e:
            self.add_system_message(f"❌ Error: {e}")
    
    def on_typing(self, event):
        """Handle typing events"""
        # Could implement typing indicators here
        pass
    
    def add_message(self, message, tag="system"):
        """Add a message to the chat display"""
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.insert(tk.END, message, tag)
        self.messages_text.see(tk.END)
        self.messages_text.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Add a system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        self.add_message(full_message, "system")
    
    def on_closing(self):
        """Handle window closing"""
        self.is_closing = True
        
        if self.client:
            self.client.disconnect()
        
        if self.root:
            self.root.destroy()
    
    def run(self):
        """Run the chat window (if standalone)"""
        if self.root:
            self.root.mainloop()