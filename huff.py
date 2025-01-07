#!/home/jean/.local/share/virtualenvs/compresseur_huffman-NA8xnzpc/bin/python
#/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module main du compresseur de huffman"""
import argparse
import logging
import os
from huffman.compresseur import compresser
from huffman.compresseur import decompresser

logger = logging.getLogger()

class CustomFormatter(logging.Formatter):
    """Formatter de logging customisé"""

    grey = "\033[0;2m"
    yellow = "\033[1;33m"
    red = "\033[31m"
    bold_red = "\033[1;31m"
    reset = "\033[0m"
    text = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: f"{grey}{text}{reset}",
        logging.INFO: f"{reset}{text}{reset}",
        logging.WARNING: f"{yellow}{text}{reset}",
        logging.ERROR: f"{red}{text}{reset}",
        logging.CRITICAL: f"{bold_red}{text}{reset}"
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

def compresser_fichier(nom_fichier_source, nom_fichier_destination):
    """Permet de compresser le fichier source en
    écrivant dans le fichier destination"""
# @u:start compresser_fichier

    with open(nom_fichier_source, 'rb') as fichier_source:
        with open(nom_fichier_destination, 'wb') as fichier_destination:
            compresser(fichier_destination, fichier_source)

# @u:end compresser_fichier

def decompresser_fichier(nom_fichier_source, nom_fichier_destination):
    """Permet de décompresser le fichier source en
    écrivant dans le fichier destination"""
# @u:start decompresser_fichier

    with open(nom_fichier_source, 'rb') as fichier_source:
        with open(nom_fichier_destination, 'wb') as fichier_destination:
            decompresser(fichier_destination, fichier_source)

# @u:end decompresser_fichier

def main():
    """progamme principal"""
# @u:start main

    parser = argparse.ArgumentParser(description="Compresseur/décompresseur d’huffman")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="""affiche des informations lors des
                            phases de compression de de décompression""")
    parser.add_argument("commande", choices=['c', 'd'],
                        help="commande : c pour compression, d pour décompression")
    parser.add_argument("nom_fichier_source",
                        help="nom du fichier à compresser ou décompresser")
    parser.add_argument("nom_fichier_destination",
                        help="nom du fichier à créer")
    args = parser.parse_args()

    sortie_standard = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    if args.verbose == 1:
        sortie_standard.setLevel(logging.INFO)
    elif args.verbose == 0:
        sortie_standard.setLevel(logging.WARNING)

    sortie_standard.setFormatter(CustomFormatter())
    logger.addHandler(sortie_standard)

    nom_fichier_source = args.nom_fichier_source
    nom_fichier_destination = args.nom_fichier_destination

    if not os.path.exists(nom_fichier_source):
        logger.error("Le fichier source '%s' n'existe pas !", nom_fichier_source)
        return
    if os.path.exists(nom_fichier_destination):
        logger.error("Le fichier destination '%s' existe déjà !", nom_fichier_destination)
        return

    if args.commande == 'c':
        compresser_fichier(nom_fichier_source, nom_fichier_destination)
    elif args.commande == 'd':
        decompresser_fichier(nom_fichier_source, nom_fichier_destination)

# @u:end main

if __name__ == "__main__":
    main()
