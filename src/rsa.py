"""
Module de cryptage RSA

Ce module fournit les fonctionnalités de cryptage RSA pour les messages cryptographiques.

Author: [Votre nom]
Date: [Date]
"""

import os
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class RSAEncryptor:
    """
    Classe d'encrypteur RSA.
    """

    def __init__(self, key_size=2048):
        """
        Initialise l'encrypteur avec une taille de clé spécifique.

        Args:
            key_size (int): Taille de la clé RSA (par défaut 2048).
        """
        self.key_size = key_size

    def generate_key_pair(self):
        """
        Génère un couple de clés RSA.

        Returns:
            tuple: Couple de clés publique et privée.
        """
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        private_key = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key = key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        return private_key, public_key

    def encrypt(self, message, public_key):
        """
        Crypte un message avec la clé publique.

        Args:
            message (bytes): Message à crypter.
            public_key (bytes): Clé publique.

        Returns:
            bytes: Message crypté.
        """
        public_key = serialization.load_ssh_public_key(
            public_key,
            backend=default_backend()
        )
        encrypted_message = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message

    def decrypt(self, encrypted_message, private_key):
        """
        Déchiffre un message avec la clé privée.

        Args:
            encrypted_message (bytes): Message crypté.
            private_key (bytes): Clé privée.

        Returns:
            bytes: Message déchiffré.
        """
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )
        decrypted_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message

    def sign(self, message, private_key):
        """
        Signe un message avec la clé privée.

        Args:
            message (bytes): Message à signer.
            private_key (bytes): Clé privée.

        Returns:
            bytes: Signature du message.
        """
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, message, signature, public_key):
        """
        Vérifie la signature d'un message.

        Args:
            message (bytes): Message à vérifier.
            signature (bytes): Signature du message.
            public_key (bytes): Clé publique.

        Returns:
            bool: Vrai si la signature est valide, faux sinon.
        """
        public_key = serialization.load_ssh_public_key(
            public_key,
            backend=default_backend()
        )
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

def main():
    # Créer un encrypteur RSA
    encryptor = RSAEncryptor()

    # Générer un couple de clés
    private_key, public_key = encryptor.generate_key_pair()

    # Crypter un message
    message = b"Bonjour, monde!"
    encrypted_message = encryptor.encrypt(message, public_key)

    # Déchiffrer le message
    decrypted_message = encryptor.decrypt(encrypted_message, private_key)

    # Signer un message
    signature = encryptor.sign(message, private_key)

    # Vérifier la signature
    is_valid = encryptor.verify_signature(message, signature, public_key)

    print(f"Message original : {message.decode()}")
    print(f"Message crypté : {encrypted_message.hex()}")
    print(f"Message déchiffré : {decrypted_message.decode()}")
    print(f"Signature : {signature.hex()}")
    print(f"Signature valide : {is_valid}")

if __name__ == "__main__":
    main()