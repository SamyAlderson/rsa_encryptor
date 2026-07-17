"""
Fichier contenant les fonctions d'aide pour le projet rsa_encryptor.
"""

import logging
import os
import numpy as np

class Util:
    """
    Classe contenant les fonctions d'aide pour le projet rsa_encryptor.
    """

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Récupère un logger avec le nom spécifié.

        Args:
        name (str): Nom du logger.

        Returns:
        logging.Logger: Logger avec le nom spécifié.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def load_file(file_path: str) -> bytes:
        """
        Charge le contenu d'un fichier.

        Args:
        file_path (str): Chemin d'accès au fichier.

        Returns:
        bytes: Contenu du fichier.

        Raises:
        FileNotFoundError: Le fichier spécifié n'existe pas.
        """
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError as e:
            logging.error(f"Le fichier '{file_path}' n'existe pas.")
            raise e

    @staticmethod
    def save_file(file_path: str, data: bytes) -> None:
        """
        Enregistre le contenu dans un fichier.

        Args:
        file_path (str): Chemin d'accès au fichier.
        data (bytes): Contenu à enregistrer.
        """
        with open(file_path, 'wb') as file:
            file.write(data)

    @staticmethod
    def generate_random_key(length: int) -> bytes:
        """
        Génère une clé aléatoire avec la longueur spécifiée.

        Args:
        length (int): Longueur de la clé.

        Returns:
        bytes: Clé aléatoire.
        """
        return np.random.bytes(length)

    @staticmethod
    def validate_input(input_data: any) -> bool:
        """
        Valide l'entrée.

        Args:
        input_data (any): Entrée à valider.

        Returns:
        bool: True si l'entrée est valide, False sinon.
        """
        # Implémentation de la validation d'entrée
        # Pour le moment, on laisse simplement passer toutes les entrées
        return True