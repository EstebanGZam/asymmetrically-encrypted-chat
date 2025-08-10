# server.py - Secure relay server
import socket
import threading
import json
import time

class SecureChatServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.clients = {}  # {username: socket}
        self.public_keys = {}  # {username: public_key_pem}
        
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(2)  # Only 2 clients for Alice and Bob
        
        print(f"🔒 Servidor seguro iniciado en {self.host}:{self.port}")
        print("💡 El servidor NO puede leer mensajes - solo actúa como relay")
        
        while len(self.clients) < 2:
            client_socket, address = server.accept()
            print(f"🔌 Nueva conexión desde {address}")
            
            client_thread = threading.Thread(
                target=self.handle_client, 
                args=(client_socket, address)
            )
            client_thread.start()
    
    def handle_client(self, client_socket, address):
        try:
            # Receive registration information
            data = client_socket.recv(4096).decode('utf-8')
            register_data = json.loads(data)
            
            username = register_data['username']
            public_key_pem = register_data['public_key']
            
            # Store client and public key
            self.clients[username] = client_socket
            self.public_keys[username] = public_key_pem
            
            print(f"✅ Usuario registrado: {username}")
            
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
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                message_data = json.loads(data)
                self.relay_message(username, message_data)
                
        except Exception as e:
            print(f"❌ Error con cliente {address}: {e}")
        finally:
            client_socket.close()
            # Remove disconnected client
            for user, sock in list(self.clients.items()):
                if sock == client_socket:
                    del self.clients[user]
                    if user in self.public_keys:
                        del self.public_keys[user]
                    print(f"🔌 Cliente {user} desconectado")
                    break
    
    def initiate_key_exchange(self):
        """Facilitate public key exchange between Alice and Bob"""
        usernames = list(self.clients.keys())
        user1, user2 = usernames[0], usernames[1]
        
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
        
        print("🔑 Intercambio de llaves públicas completado")
    
    def relay_message(self, sender, message_data):
        """Relay encrypted messages (server cannot read them)"""
        for username, client_socket in self.clients.items():
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
                    print(f"📨 Mensaje relay: {sender} -> {username} (ENCRIPTADO)")
                except Exception as e:
                    print(f"❌ Error enviando mensaje a {username}: {e}")