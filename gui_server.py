# gui_server.py - GUI adaptation of secure relay server
import socket
import threading
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv('HOST', 'localhost')
SERVER_PORT = int(os.getenv('PORT', 8888))


class GUISecureChatServer:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.clients = {}  # {username: socket}
        self.public_keys = {}  # {username: public_key_pem}
        self.running = False
        self.server_socket = None
        self.gui_callback = None
        self.messages_relayed = 0
        
    def set_gui_callback(self, callback):
        """Set callback for GUI updates"""
        self.gui_callback = callback
        
    def start(self):
        """Start the relay server"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)  # Allow up to 5 connections
            
            if self.gui_callback:
                self.gui_callback("server_started", {
                    "host": self.host, 
                    "port": self.port
                })
            
            while self.running:
                try:
                    self.server_socket.settimeout(1)  # Short timeout for responsiveness
                    client_socket, address = self.server_socket.accept()
                    
                    if self.gui_callback:
                        self.gui_callback("new_connection", {"address": address})
                    
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running and self.gui_callback:
                        self.gui_callback("error", {"message": f"Error aceptando conexión: {e}"})
                    break
                    
        except Exception as e:
            if self.gui_callback:
                self.gui_callback("error", {"message": f"Error iniciando servidor: {e}"})
        finally:
            self.cleanup()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        username = None
        try:
            # Set socket timeout
            client_socket.settimeout(30)
            
            # Receive registration information
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return
                
            register_data = json.loads(data)
            username = register_data['username']
            public_key_pem = register_data['public_key']
            
            # Store client and public key
            self.clients[username] = client_socket
            self.public_keys[username] = public_key_pem
            
            # Notify GUI
            if self.gui_callback:
                self.gui_callback("client_connected", {
                    "username": username,
                    "address": f"{address[0]}:{address[1]}",
                    "total_clients": len(self.clients)
                })
            
            # Send registration confirmation
            response = {
                'type': 'registration_success',
                'message': f'Bienvenido {username}!'
            }
            client_socket.send(json.dumps(response).encode('utf-8'))
            
            # If 2 users, start key exchange
            if len(self.clients) == 2:
                self.initiate_key_exchange()
            
            # Listen for messages
            while self.running:
                try:
                    client_socket.settimeout(1)
                    data = client_socket.recv(4096).decode('utf-8')
                    if not data:
                        break
                        
                    message_data = json.loads(data)
                    self.relay_message(username, message_data)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running and self.gui_callback:
                        self.gui_callback("error", {"message": f"Error con cliente {username}: {e}"})
                    break
                    
        except Exception as e:
            if self.gui_callback:
                self.gui_callback("error", {"message": f"Error manejando cliente {address}: {e}"})
        finally:
            # Cleanup client connection
            try:
                client_socket.close()
            except:
                pass
                
            # Remove disconnected client
            if username and username in self.clients:
                del self.clients[username]
                if username in self.public_keys:
                    del self.public_keys[username]
                    
                if self.gui_callback:
                    self.gui_callback("client_disconnected", {
                        "username": username,
                        "total_clients": len(self.clients)
                    })
    
    def initiate_key_exchange(self):
        """Facilitate public key exchange between clients"""
        if len(self.clients) < 2:
            return
            
        usernames = list(self.clients.keys())
        user1, user2 = usernames[0], usernames[1]
        
        try:
            # Send user2's public key to user1
            key_exchange_msg1 = {
                'type': 'key_exchange',
                'from': user2,
                'public_key': self.public_keys[user2]
            }
            self.clients[user1].send(json.dumps(key_exchange_msg1).encode('utf-8'))
            
            # Send user1's public key to user2
            key_exchange_msg2 = {
                'type': 'key_exchange',
                'from': user1,
                'public_key': self.public_keys[user1]
            }
            self.clients[user2].send(json.dumps(key_exchange_msg2).encode('utf-8'))
            
            # Notify GUI
            if self.gui_callback:
                self.gui_callback("key_exchange", {
                    "user1": user1,
                    "user2": user2
                })
                
        except Exception as e:
            if self.gui_callback:
                self.gui_callback("error", {"message": f"Error en intercambio de llaves: {e}"})
    
    def relay_message(self, sender, message_data):
        """Relay encrypted messages (server cannot read them)"""
        relayed_to = []
        
        for username, client_socket in list(self.clients.items()):
            if username != sender:
                try:
                    relay_msg = {
                        'type': 'encrypted_message',
                        'from': sender,
                        'encrypted_content': message_data['encrypted_content'],
                        'signature': message_data['signature'],
                        'timestamp': time.time()
                    }
                    client_socket.send(json.dumps(relay_msg).encode('utf-8'))
                    relayed_to.append(username)
                    
                except Exception as e:
                    if self.gui_callback:
                        self.gui_callback("error", {"message": f"Error enviando mensaje a {username}: {e}"})
        
        # Update message count and notify GUI
        self.messages_relayed += 1
        if self.gui_callback and relayed_to:
            for receiver in relayed_to:
                self.gui_callback("message_relay", {
                    "sender": sender,
                    "receiver": receiver
                })
    
    def stop(self):
        """Stop the server"""
        self.running = False
        
        # Close all client connections
        for client_socket in list(self.clients.values()):
            try:
                client_socket.close()
            except:
                pass
        
        self.clients.clear()
        self.public_keys.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        if self.gui_callback:
            self.gui_callback("server_stopped", {})
    
    def cleanup(self):
        """Clean up server resources"""
        self.running = False
        
        # Close all connections
        for client_socket in list(self.clients.values()):
            try:
                client_socket.close()
            except:
                pass
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        self.clients.clear()
        self.public_keys.clear()
    
    def get_stats(self):
        """Get server statistics"""
        return {
            "connected_clients": len(self.clients),
            "messages_relayed": self.messages_relayed,
            "running": self.running,
            "clients_list": list(self.clients.keys())
        }