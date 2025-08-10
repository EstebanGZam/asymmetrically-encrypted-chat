# gui_client.py - GUI adaptation of secure chat client
import socket
import threading
import json
import time
from datetime import datetime
from crypto_utils import CryptoManager

class GUISecureChatClient:
    def __init__(self, username, gui_callback=None):
        self.username = username
        self.crypto = CryptoManager()
        self.socket = None
        self.connected = False
        self.peer_username = None
        self.gui_callback = gui_callback
        
    def connect(self, host='localhost', port=8888):
        """Connect to server and register user"""
        try:
            # Generate keypair
            self.crypto.generate_keypair()
            
            # Get fingerprint
            fingerprint = self.crypto.get_public_key_fingerprint()
            
            # Connect to server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            self.socket.connect((host, port))
            
            # Register user by sending public key
            register_data = {
                'username': self.username,
                'public_key': self.crypto.get_public_key_pem().decode('utf-8')
            }
            self.socket.send(json.dumps(register_data).encode('utf-8'))
            
            # Set connected BEFORE starting the thread
            self.connected = True
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            # Notify GUI
            if self.gui_callback:
                self.gui_callback("status", {"message": f"Conectado como {self.username}"})
                self.gui_callback("status", {"message": f"Tu fingerprint: {fingerprint}"})
            
            return True
            
        except Exception as e:
            self.connected = False
            if self.gui_callback:
                self.gui_callback("error", f"Error de conexión: {e}")
            return False
    
    def receive_messages(self):
        """Thread to receive messages from server"""
        while self.connected:
            try:
                self.socket.settimeout(1)  # Short timeout for responsiveness
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                message = json.loads(data)
                self.handle_received_message(message)
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.connected and self.gui_callback:
                    self.gui_callback("error", f"Error recibiendo mensaje: {e}")
                break
    
    def handle_received_message(self, message):
        """Handle messages received from server"""
        msg_type = message.get('type')
        
        if msg_type == 'registration_success':
            if self.gui_callback:
                self.gui_callback("status", {"message": message['message']})
                
        elif msg_type == 'key_exchange':
            # Receive peer's public key
            self.peer_username = message['from']
            peer_public_key_pem = message['public_key'].encode('utf-8')
            self.crypto.load_peer_public_key(peer_public_key_pem)
            
            # Get peer's fingerprint for verification
            peer_fingerprint = self.crypto.get_public_key_fingerprint(self.crypto.peer_public_key)
            
            # Notify GUI
            if self.gui_callback:
                self.gui_callback("key_exchange", {
                    "peer_name": self.peer_username,
                    "fingerprint": peer_fingerprint
                })
                
        elif msg_type == 'encrypted_message':
            # Decrypt and verify message
            try:
                sender = message['from']
                encrypted_content = message['encrypted_content']
                signature = message['signature']
                timestamp = datetime.fromtimestamp(message['timestamp'])
                
                # Decrypt message
                decrypted_message = self.crypto.decrypt_message(encrypted_content)
                
                # Verify signature
                signature_valid = self.crypto.verify_signature(decrypted_message, signature)
                
                # Notify GUI
                if self.gui_callback:
                    self.gui_callback("message", {
                        "sender": sender,
                        "message": decrypted_message,
                        "timestamp": timestamp,
                        "signature_valid": signature_valid
                    })
                    
            except Exception as e:
                if self.gui_callback:
                    self.gui_callback("error", f"Error procesando mensaje: {e}")
    
    def send_message(self, message):
        """Send encrypted message"""
        if not self.crypto.peer_public_key:
            if self.gui_callback:
                self.gui_callback("error", "No se puede enviar mensaje: llave del peer no disponible")
            return False
            
        try:
            # Encrypt message
            encrypted_content = self.crypto.encrypt_message(message)
            
            # Sign message
            signature = self.crypto.sign_message(message)
            
            # Send to server
            message_data = {
                'encrypted_content': encrypted_content,
                'signature': signature
            }
            self.socket.send(json.dumps(message_data).encode('utf-8'))
            
            return True
            
        except Exception as e:
            if self.gui_callback:
                self.gui_callback("error", f"Error enviando mensaje: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        if self.gui_callback:
            self.gui_callback("status", {"message": "Desconectado del servidor"})