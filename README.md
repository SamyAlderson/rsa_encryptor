# rsa_encryptor
Projet: Implémentation d'un encrypteur RSA pour les messages cryptographiques

## Description
Cet projet implémente un encrypteur RSA pour les messages cryptographiques en Python.
Il inclut la génération de clés RSA, le cryptage et le déchiffrement de messages, ainsi que la vérification de signatures.

## Fichiers

### `src/main.py`
Fichier principal du projet.

### `src/rsa.py`
Fichier contenant les fonctions de cryptage RSA.

### `src/utils.py`
Fichier contenant les fonctions d'aide.

### `tests/test_rsa.py`
Fichier de tests pour les fonctions de cryptage.

## Caractéristiques

### Génération de clés RSA
Cette fonction génère des clés RSA pour un message donné.

### Cryptage de messages avec RSA
Cette fonction crypte un message donné en utilisant les clés RSA générées.

### Déchiffrement de messages avec RSA
Cette fonction déchiffre un message crypté en utilisant les clés RSA.

### Vérification de signatures
Cette fonction vérifie la signature d'un message donné.

## Dépendances

### cryptography
Bibliothèque pour les opérations cryptographiques.

### numpy
Bibliothèque pour les calculs numériques.

## Exécution

Pour exécuter le projet, téléchargez les dépendances nécessaires en utilisant pip:
```bash
pip install -r requirements.txt
```
Ensuite, exécutez le fichier principal:
```bash
python src/main.py
```
## Auteur
[Votre nom]
[Votre adresse e-mail]

## Licence
Ceci est un logiciel libre, distribué sous la licence [Your License].
```

```python
import os
import sys
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def generate_keys():
    """
    Générer des clés RSA pour un message donné.

    Retourne:
        - publicKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey): Clé publique RSA
        - privateKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey): Clé privée RSA
    """
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    publicKey = key.public_key()
    return publicKey, key

def encrypt_message(publicKey, message):
    """
    Crypter un message donné en utilisant les clés RSA.

    Paramètres:
        - publicKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey): Clé publique RSA
        - message (str): Message à crypter

    Retourne:
        - encryptedMessage (bytes): Message crypté
    """
    encryptedMessage = publicKey.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encryptedMessage

def decrypt_message(privateKey, encryptedMessage):
    """
    Déchiffrer un message crypté en utilisant les clés RSA.

    Paramètres:
        - privateKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey): Clé privée RSA
        - encryptedMessage (bytes): Message crypté

    Retourne:
        - message (str): Message déchiffré
    """
    message = privateKey.decrypt(
        encryptedMessage,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message

def sign_message(privateKey, message):
    """
    Signer un message donné en utilisant les clés RSA.

    Paramètres:
        - privateKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey): Clé privée RSA
        - message (str): Message à signer

    Retourne:
        - signature (bytes): Signature du message
    """
    signature = privateKey.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(publicKey, message, signature):
    """
    Vérifier la signature d'un message donné.

    Paramètres:
        - publicKey (cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey): Clé publique RSA
        - message (str): Message à vérifier
        - signature (bytes): Signature du message

    Retourne:
        - True si la signature est valide, False sinon
    """
    try:
        publicKey.verify(
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
```

```python
import unittest
from unittest.mock import Mock
from cryptography.hazmat.backends import default_backend
from rsa_encryptor import rsa

class TestRSA(unittest.TestCase):
    def test_generate_keys(self):
        publicKey, privateKey = rsa.generate_keys()
        self.assertIsInstance(publicKey, rsa.RSAPublicKey)
        self.assertIsInstance(privateKey, rsa.RSAPrivateKey)

    def test_encrypt_message(self):
        publicKey, privateKey = rsa.generate_keys()
        message = b"Hello, World!"
        encryptedMessage = rsa.encrypt_message(publicKey, message)
        self.assertIsInstance(encryptedMessage, bytes)

    def test_decrypt_message(self):
        publicKey, privateKey = rsa.generate_keys()
        message = b"Hello, World!"
        encryptedMessage = rsa.encrypt_message(publicKey, message)
        decryptedMessage = rsa.decrypt_message(privateKey, encryptedMessage)
        self.assertEqual(message, decryptedMessage)

    def test_sign_message(self):
        publicKey, privateKey = rsa.generate_keys()
        message = b"Hello, World!"
        signature = rsa.sign_message(privateKey, message)
        self.assertIsInstance(signature, bytes)

    def test_verify_signature(self):
        publicKey, privateKey = rsa.generate_keys()
        message = b"Hello, World!"
        signature = rsa.sign_message(privateKey, message)
        self.assertTrue(rsa.verify_signature(publicKey, message, signature))

if __name__ == "__main__":
    unittest.main()