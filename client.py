# client.py - Secure chat client
import socket
import threading
import json
import time
from datetime import datetime
from crypto_utils import CryptoManager

class SecureChatClient:
    def __init__(self, username):
        self.username = username
        self.crypto = CryptoManager()
        self.socket = None
        self.connected = False
        self.peer_username = None
        
    def connect(self, host='localhost', port=8888):
        """Connect to server and register user"""
        try:
            # Generate keypair
            print("🔐 Generando par de llaves RSA...")
            self.crypto.generate_keypair()
            
            # Show our public key fingerprint
            fingerprint = self.crypto.get_public_key_fingerprint()
            print(f"🔍 Tu fingerprint de llave pública:")
            print(f"    {fingerprint}")
            
            # Connect to server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            # Register user by sending public key
            register_data = {
                'username': self.username,
                'public_key': self.crypto.get_public_key_pem().decode('utf-8')
            }
            self.socket.send(json.dumps(register_data).encode('utf-8'))
            
            # FIX: Set connected BEFORE starting the thread to avoid race condition
            self.connected = True
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            print(f"✅ Conectado como {self.username}")
            
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
    
    def receive_messages(self):
        """Thread to receive messages from server"""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                message = json.loads(data)
                self.handle_received_message(message)
                
            except Exception as e:
                if self.connected:
                    print(f"❌ Error recibiendo mensaje: {e}")
                break
    
    def handle_received_message(self, message):
        """Handle messages received from server"""
        msg_type = message.get('type')
        
        if msg_type == 'registration_success':
            print(f"🎉 {message['message']}")
            
        elif msg_type == 'key_exchange':
            # Receive peer's public key
            self.peer_username = message['from']
            peer_public_key_pem = message['public_key'].encode('utf-8')
            self.crypto.load_peer_public_key(peer_public_key_pem)
            
            # Show peer's fingerprint for verification
            peer_fingerprint = self.crypto.get_public_key_fingerprint(self.crypto.peer_public_key)
            print(f"\n🔑 Intercambio de llaves con {self.peer_username}")
            print(f"🔍 Fingerprint de {self.peer_username}:")
            print(f"    {peer_fingerprint}")
            print("⚠️  IMPORTANTE: Verifica este fingerprint con tu contacto por un canal seguro!")
            print("💬 Escribe 'verify' para confirmar verificación y habilitar el chat seguro")
            print("📝 O escribe mensajes directamente (sin verificar, bajo tu responsabilidad)")
            
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
                signature_indicator = "✅" if signature_valid else "❌"
                
                print(f"\n{timestamp.strftime('%H:%M:%S')} {signature_indicator} {sender}: {decrypted_message}")
                
                if not signature_valid:
                    print("⚠️  ADVERTENCIA: Firma digital inválida!")
                    
            except Exception as e:
                print(f"❌ Error procesando mensaje: {e}")
    
    def send_message(self, message):
        """Send encrypted message"""
        if not self.crypto.peer_public_key:
            print("❌ No se puede enviar mensaje: llave del peer no disponible")
            return
            
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
            
            # Show sent message
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{timestamp} ✅ Tú: {message}")
            
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
    
    def start_chat(self):
        """Start main chat loop"""
        if not self.connected:
            print("❌ No conectado al servidor")
            return
            
        print("\n💬 Chat iniciado. Esperando intercambio de llaves...")
        verified = False
        
        try:
            while True:
                message = input()
                if message.lower() == 'quit':
                    break
                elif message.lower() == 'verify':
                    if self.peer_username:
                        verified = True
                        print("✅ Verificación confirmada. Chat seguro establecido!")
                        print("💬 Ya puedes enviar mensajes seguros.")
                    else:
                        print("❌ No hay peer para verificar aún")
                elif message.strip():
                    if not verified and self.peer_username:
                        print("⚠️  Advertencia: Enviando mensaje sin verificar fingerprint")
                    self.send_message(message)
                    
        except KeyboardInterrupt:
            print("\n👋 Cerrando chat...")
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.socket:
            self.socket.close()
        print("🔌 Desconectado del servidor")