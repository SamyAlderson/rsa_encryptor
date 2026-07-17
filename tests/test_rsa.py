# tests/test_rsa.py

"""
Fichier de tests pour les fonctions de cryptage RSA
"""

import unittest
from unittest.mock import Mock
from rsa import generate_keypair, encrypt, decrypt
from rsa.exceptions import RSAError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

class TestRSA(unittest.TestCase):
    def test_generate_keypair(self):
        """
        Tests la génération d'une paire de clés RSA
        """
        public_key, private_key = generate_keypair()
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

    def test_encrypt_decrypt(self):
        """
        Tests le cryptage et le déchiffrement d'un message avec RSA
        """
        public_key, private_key = generate_keypair()
        message = b"Bonjour, monde !"
        encrypted_message = encrypt(public_key, message)
        decrypted_message = decrypt(private_key, encrypted_message)
        self.assertEqual(message, decrypted_message)

    def test_encrypt_with_invalid_key(self):
        """
        Tests l'échec du cryptage avec une clé invalide
        """
        public_key, private_key = generate_keypair()
        invalid_key = Mock()
        with self.assertRaises(RSAError):
            encrypt(invalid_key, b"Bonjour, monde !")

    def test_decrypt_with_invalid_key(self):
        """
        Tests l'échec du déchiffrement avec une clé invalide
        """
        public_key, private_key = generate_keypair()
        invalid_key = Mock()
        with self.assertRaises(RSAError):
            decrypt(invalid_key, b"Bonjour, monde !")

    def test_sign_verify(self):
        """
        Tests la signature et la vérification d'une signature avec RSA
        """
        public_key, private_key = generate_keypair()
        message = b"Bonjour, monde !"
        signature = private_key.sign(message)
        self.assertTrue(public_key.verify(signature, message))

    def test_sign_verify_with_invalid_key(self):
        """
        Tests l'échec de la vérification d'une signature avec une clé invalide
        """
        public_key, private_key = generate_keypair()
        invalid_key = Mock()
        message = b"Bonjour, monde !"
        signature = private_key.sign(message)
        with self.assertRaises(RSAError):
            invalid_key.verify(signature, message)

if __name__ == "__main__":
    unittest.main()
```

```python
# rsa.py

"""
Fichier contenant les fonctions de cryptage RSA
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class RSAError(Exception):
    pass

def generate_keypair():
    """
    Génère une paire de clés RSA
    """
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = key.public_key()
    return public_key, key

def encrypt(public_key, message):
    """
    Crypte un message avec la clé publique RSA
    """
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt(private_key, encrypted_message):
    """
    Déchiffre un message crypté avec la clé privée RSA
    """
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def sign(private_key, message):
    """
    Signe un message avec la clé privée RSA
    """
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify(public_key, signature, message):
    """
    Vérifie une signature avec la clé publique RSA
    """
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