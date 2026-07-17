"""
Fichier principal du projet rsa_encryptor.

Ce fichier contient la logique d'entrée du projet, permettant de générer des clés RSA,
de crypter et de déchiffrer des messages, ainsi que de vérifier des signatures.
"""

import os
import argparse
from rsa import generate_keypair, encrypt, decrypt, verify_signature
from utils import load_private_key, load_public_key
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def main():
    """
    Fonction principale du projet.

    Cette fonction permet de gérer les différentes étapes de cryptage et de déchiffrement.
    Elle prend en compte les arguments de ligne de commande pour déterminer l'action à effectuer.
    """
    parser = argparse.ArgumentParser(description="rsa_encryptor")
    subparsers = parser.add_subparsers(dest="action")

    # Génération de clés RSA
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("-p", "--public", action="store_true", help="Générer une paire de clés")
    generate_parser.add_argument("-s", "--secret", action="store_true", help="Générer une paire de clés")

    # Cryptage et déchiffrement
    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("-p", "--public", action="store_true", help="Utiliser la clé publique")
    encrypt_parser.add_argument("-s", "--secret", action="store_true", help="Utiliser la clé secrète")
    encrypt_parser.add_argument("-d", "--data", required=True, help="Données à crypter")

    # Vérification de signature
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("-p", "--public", action="store_true", help="Utiliser la clé publique")
    verify_parser.add_argument("-s", "--secret", action="store_true", help="Utiliser la clé secrète")
    verify_parser.add_argument("-d", "--data", required=True, help="Données à vérifier")
    verify_parser.add_argument("-s", "--signature", required=True, help="Signature à vérifier")

    args = parser.parse_args()

    if args.action == "generate":
        if args.public and args.secret:
            keypair = generate_keypair()
            private_key = keypair.private_key
            public_key = keypair.public_key
            with open("private.pem", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            with open("public.pem", "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
        elif args.public:
            private_key = load_private_key()
            public_key = generate_keypair().public_key
            with open("public.pem", "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
        elif args.secret:
            public_key = load_public_key()
            private_key = generate_keypair().private_key
            with open("private.pem", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        else:
            parser.print_help()

    elif args.action == "encrypt":
        if args.public:
            public_key = load_public_key()
            encrypted_data = encrypt(args.data.encode("utf-8"), public_key)
            print(encrypted_data.hex())
        elif args.secret:
            private_key = load_private_key()
            encrypted_data = encrypt(args.data.encode("utf-8"), private_key)
            print(encrypted_data.hex())
        else:
            parser.print_help()

    elif args.action == "verify":
        if args.public:
            public_key = load_public_key()
            try:
                verify_signature(args.data.encode("utf-8"), args.signature.encode("utf-8"), public_key)
                print("Signature valide")
            except InvalidSignature:
                print("Signature invalide")
        elif args.secret:
            private_key = load_private_key()
            try:
                verify_signature(args.data.encode("utf-8"), args.signature.encode("utf-8"), private_key)
                print("Signature valide")
            except InvalidSignature:
                print("Signature invalide")
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
```

```python
"""
Fichier contenant les fonctions de cryptage RSA.

Ce fichier contient les fonctions pour générer des clés RSA, pour crypter et déchiffrer des messages,
ainsi que pour vérifier des signatures.
"""

import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_keypair():
    """
    Fonction pour générer une paire de clés RSA.

    Cette fonction retourne une paire de clés RSA.
    """
    keypair = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return keypair

def load_private_key():
    """
    Fonction pour charger une clé privée RSA.

    Cette fonction retourne la clé privée RSA chargée à partir du fichier "private.pem".
    """
    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key():
    """
    Fonction pour charger une clé publique RSA.

    Cette fonction retourne la clé publique RSA chargée à partir du fichier "public.pem".
    """
    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key
```

```python
"""
Fichier contenant les fonctions d'aide.

Ce fichier contient les fonctions pour aider les autres fichiers du projet.
"""

def encrypt(data, key):
    """
    Fonction pour crypter des données avec une clé RSA.

    Cette fonction prend en compte les données à crypter et la clé RSA à utiliser.
    Elle retourne les données cryptées sous forme de bytes.
    """
    encrypted_data = key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def decrypt(encrypted_data, key):
    """
    Fonction pour déchiffrer des données cryptées avec une clé RSA.

    Cette fonction prend en compte les données cryptées et la clé RSA à utiliser.
    Elle retourne les données déchiffrées sous forme de bytes.
    """
    decrypted_data = key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

def verify_signature(data, signature, key):
    """
    Fonction pour vérifier une signature avec une clé RSA.

    Cette fonction prend en compte les données, la signature et la clé RSA à utiliser.
    Elle retourne True si la signature est valide, False sinon.
    """
    key.verify(
        signature,
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return True