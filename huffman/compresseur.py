#!/usr/bin/env python3
""" Module compresseur """
from typing import Dict
import io
import logging
from huffman.compteur import Compteur
from huffman.arbre_huffman import ArbreHuffman
from huffman.file_de_priorite import FileDePriorite
from huffman.code_binaire import CodeBinaire, Bit

LOGGER = logging.getLogger()

NB_OCTETS_CODAGE_INT = 4

# @u:start precedentTP

def statistiques(source: io.BufferedReader) -> (Compteur, int):
    """ fonction qui retourne le nombre d'occurences (Compteur)
d'un flux d'octets et ainsi que le nombre d'octets"""
    LOGGER.info("Création des statistiques")
    cpt: Compteur = Compteur()
    longueur: int = 0
    source.seek(0)
    for les_octets in source:
        for octet_unique in les_octets:
            cpt.incrementer(octet_unique)
            longueur += 1
    LOGGER.debug("Statistiques du fichier source :\n%s", cpt)
    return cpt, longueur

def arbre_de_huffman(stat: Compteur) -> ArbreHuffman:
    """ fonction qui retourne un arbre d'huffman à partir d'un compteur """
    LOGGER.info("Création de l'arbre de Huffman")
    file = FileDePriorite(cle=lambda a: a.nb_occurrences)
    for octet in range(256):
        if (nb := stat.nb_occurrences(octet)) > 0:
            arbre: ArbreHuffman = ArbreHuffman(element=octet, nb_occurrences=nb)
            file.enfiler(arbre)
    while len(file) >= 2:
        file.enfiler(file.defiler() + file.defiler())
    arbre_res: ArbreHuffman = file.defiler()
    LOGGER.debug("Arbre de Huffman : \n%s", arbre_res)
    return arbre_res

def codes_binaire(arbre: ArbreHuffman) -> Dict[int, CodeBinaire]:
    """ fonction qui retourne le code binaire de tous les éléments
d'un arbre d'Huffman """
    LOGGER.info("Création des codes binaires")
    def codes_binaires_rec(arbre: ArbreHuffman, code_courant: CodeBinaire, \
                           table: Dict[int, CodeBinaire]):
        if arbre.est_une_feuille:
            table[arbre.element] = code_courant
        else:
            codes_binaires_rec(arbre.fils_gauche, code_courant + CodeBinaire(Bit.BIT_0), table)
            codes_binaires_rec(arbre.fils_droit, code_courant + CodeBinaire(Bit.BIT_1), table)
    table: Dict[int, CodeBinaire] = {}
    codes_binaires_rec(arbre.fils_gauche, CodeBinaire(Bit.BIT_0), table)
    codes_binaires_rec(arbre.fils_droit, CodeBinaire(Bit.BIT_1), table)
    return table

def compresser(destination: io.RawIOBase,
               source: io.RawIOBase,
               nb_octets_pour_serialisation_des_int: int=4,
               ordre_pour_serialisation_des_int='big') -> None:
    """ fonction qui compresse les données de source dans destination """

    def obtenir_type_de_fichier(stats: Compteur) -> int:
        """Permet d'obtenir le type d'un fichier (0,1 ou 2) en connaissant ses statistiques"""
        if len(stats.elements) == 0:
            return 0
        if len(stats.elements) <= 2:
            return 1
        return 2

    LOGGER.info("Compression")
    destination.seek(0)
    destination.write(b"\x34\x32")

    stats, longueur = statistiques(source)
    LOGGER.debug("Longueur du fichier source : %s octets", longueur)

    if obtenir_type_de_fichier(stats) == 0:
        LOGGER.info("Fichier vide")
        destination.write(b"\x00")
        LOGGER.info("Écriture du fichier compressé")
        LOGGER.debug("Fin de l'écriture")
        return

    if obtenir_type_de_fichier(stats) == 1:
        LOGGER.info("N fois le même octet")
        destination.write(b"\x01")
        octet: int = list(stats.elements_plus_frequents())[0]
        LOGGER.debug("Octet présent : %s (%s), %s occurrences", \
                     octet, chr(octet), stats.nb_occurrences(octet))
        LOGGER.info("Écriture du fichier compressé")
        LOGGER.debug("Écriture du nombre d'occurrences")
        destination.write(stats.nb_occurrences(octet)\
                          .to_bytes(nb_octets_pour_serialisation_des_int, \
                                    ordre_pour_serialisation_des_int))
        LOGGER.debug("Écriture de l'octet %s", octet)
        destination.write(bytes([octet]))
        LOGGER.debug("Fin de l'écriture")
        return

    LOGGER.info("Cas général")
    destination.write(b"\x02")
    codes: Dict[int, CodeBinaire] = codes_binaire(arbre_de_huffman(stats))
    LOGGER.debug("Codes binaires des octets : \n%s", \
                {oct:str(code) for (oct,code) in codes.items()})
    LOGGER.info("Écriture du fichier compressé")
    destination.write(longueur.to_bytes(nb_octets_pour_serialisation_des_int, \
                                        ordre_pour_serialisation_des_int))
    LOGGER.debug("Écriture de la longueur : %s", longueur)

    LOGGER.debug("Écriture des statistiques")
    for octet in range(256):
        occurrences: int = stats.nb_occurrences(octet) if octet in stats.elements else 0
        destination.write(occurrences.to_bytes(nb_octets_pour_serialisation_des_int, \
                                               ordre_pour_serialisation_des_int))

    source.seek(0)
    buffer: int = 0
    bit_courant: int = 0
    LOGGER.debug("Écriture des codes binaires")
    for les_octets in source:
        for octet_unique in les_octets:                 # on écrit chaque bit
            for bit in codes[octet_unique]:             # du code binaire dans le buffer
                if bit == Bit.BIT_1:                        # si le bit est 1 :
                    buffer: int = buffer|2**(bit_courant)   # on force le bit courant du buffer à 1
                bit_courant += 1
                if bit_courant >= 8:                    # lorsque le buffer est plein :
                    destination.write(bytes([buffer]))
                    bit_courant: int = 0
                    buffer: int = 0
    if buffer != 0:
        destination.write(bytes([buffer]))
    LOGGER.debug("Fin de l'écriture")

# @u:end precedentTP

def decompresser(destination: io.RawIOBase,
                 source: io.RawIOBase,
                 nb_octets_pour_serialisation_des_int: int=4,
                 ordre_pour_serialisation_des_int='big') -> None:
    """ fichier qui décompresse les données destination dans source """
# @u:start decompresser
    LOGGER.info("Decompression")
    source.seek(0)
    destination.seek(0)
    LOGGER.debug("Lecture de l'identifiant du fichier")
    if source.readline(2) != b"\x34\x32" :
        LOGGER.error("Le fichier source n'est pas un fichier compressé")
        return
    LOGGER.debug("Lecture du type de fichier")
    type_fichier: int = int.from_bytes(source.readline(1), \
                                       byteorder=ordre_pour_serialisation_des_int)
    LOGGER.debug("type = %s", type_fichier)
    if type_fichier == 0:
        LOGGER.info("Fichier vide")
        LOGGER.info("Création du fichier décompressé")
        LOGGER.debug("Fin de l'écriture")
        return

    LOGGER.debug("Lecture de la longueur du fichier initial")
    longueur: int = int.from_bytes(source.readline(nb_octets_pour_serialisation_des_int), \
                              byteorder=ordre_pour_serialisation_des_int)
    LOGGER.debug("longueur = %s", longueur)

    if type_fichier == 1:
        LOGGER.info("N fois le même octet")
        LOGGER.info("Création du fichier décompressé")
        LOGGER.debug("Lecture de l'octet")
        octet: bytes = source.readline(1)
        LOGGER.debug("Écriture de l'octet %s, %s fois", octet, longueur)
        for _ in range(longueur):
            destination.write(octet)
        LOGGER.debug("Écriture d'un octet de fin de ligne : (10)")
        destination.write(bytes([10]))
        LOGGER.debug("Fin de l'écriture")
        return

    LOGGER.info("Cas général")
    stats: Compteur = Compteur()
    LOGGER.info("Lecture des statistiques")
    for octet in range(256):
        occurrences: int = int.from_bytes(source.readline(nb_octets_pour_serialisation_des_int), \
                                          byteorder=ordre_pour_serialisation_des_int)
        if occurrences > 0:
            stats.fixer(octet, occurrences)

    arbre: ArbreHuffman = arbre_de_huffman(stats)
    octet_courant: bytes = source.readline(1)
    bit_courant: int = 0
    arbre_courant: ArbreHuffman = arbre
    LOGGER.info("Création du fichier décompressé")
    for _ in range(longueur):
        while not arbre_courant.est_une_feuille:
            if bit_courant > 7:
                bit_courant: int = 0
                octet_courant: bytes = source.readline(1)
            if (int.from_bytes(octet_courant, \
                               byteorder=ordre_pour_serialisation_des_int)&2**(bit_courant))==0:
                arbre_courant: ArbreHuffman = arbre_courant.fils_gauche
            else:
                arbre_courant: ArbreHuffman = arbre_courant.fils_droit
            bit_courant += 1
        destination.write(arbre_courant.element.to_bytes(1, ordre_pour_serialisation_des_int))
        arbre_courant: ArbreHuffman = arbre
    LOGGER.debug("Fin de l'écriture")

# @u:end decompresser

if __name__ == "__main__":
    pass
