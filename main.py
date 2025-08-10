import sys
from server import SecureChatServer
from client import SecureChatClient

def main():
    print("Sistema de Chat Seguro con Cifrado Asimétrico")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # Run server
        server = SecureChatServer()
        try:
            server.start()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
    else:
        # Run client
        username = input("Ingresa tu nombre de usuario: ").strip()
        if not username:
            print("Nombre de usuario requerido")
            return
            
        client = SecureChatClient(username)
        client.connect()
        
        if client.connected:
            client.start_chat()

if __name__ == "__main__":
    main()