import base64
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import os

class CryptoManager:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.peer_public_key = None
        
    def generate_keypair(self):
        """Generate RSA 2048-bit keypair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        print("Par de llaves generado exitosamente")
        
    def get_public_key_pem(self):
        """Return public key in PEM format for sharing"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def load_peer_public_key(self, pem_data):
        """Load peer's public key"""
        self.peer_public_key = load_pem_public_key(pem_data)
        print("Llave pública del peer cargada")
    
    def get_public_key_fingerprint(self, public_key=None):
        """Generate SHA-256 fingerprint of public key for verification"""
        if public_key is None:
            public_key = self.public_key
        
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        fingerprint = hashlib.sha256(pem_data).hexdigest()
        # Readable format: AA:BB:CC:DD...
        return ':'.join(fingerprint[i:i+2] for i in range(0, len(fingerprint), 2))
    
    def encrypt_message(self, message):
        """Encrypt message using peer's public key"""
        if not self.peer_public_key:
            raise ValueError("Peer's public key not loaded")
            
        message_bytes = message.encode('utf-8')
        
        # RSA has size limit, use OAEP padding
        ciphertext = self.peer_public_key.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt_message(self, encrypted_message):
        """Decrypt message using our private key"""
        if not self.private_key:
            raise ValueError("Private key not generated")
            
        ciphertext = base64.b64decode(encrypted_message.encode('utf-8'))
        
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')
    
    def sign_message(self, message):
        """Sign message with our private key"""
        message_bytes = message.encode('utf-8')
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, message, signature):
        """Verify message signature using peer's public key"""
        if not self.peer_public_key:
            raise ValueError("Peer's public key not loaded")
            
        try:
            message_bytes = message.encode('utf-8')
            signature_bytes = base64.b64decode(signature.encode('utf-8'))
            
            self.peer_public_key.verify(
                signature_bytes,
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False