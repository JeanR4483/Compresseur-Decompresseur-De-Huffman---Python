#!/usr/bin/env python3
""" Module proposant la classe ArbreHuffman """

from functools import total_ordering
from typing import TypeVar, Self

T = TypeVar('T')

class ArbreHuffmanErreur(Exception):
    """Erreurs relatives aux arbres de huffman"""


class DoitEtreUneFeuilleErreur(ArbreHuffmanErreur):
    """Erreur lorsqu'un arbre est un noeud alors qu'il doit être une feuille"""


class NeDoitPasEtreUneFeuilleErreur(ArbreHuffmanErreur):
    """Erreur lorsqu'un arbre est une feuille alors qu'il doit être un noeud"""


class ArbreHuffmanIncoherentErreur(ArbreHuffmanErreur):
    """Erreur lorsqu'un arbre est incohérent"""

@total_ordering
class ArbreHuffman[T]:
    """ArbreHuffman permet de représenter un arbre de huffman"""

    def __init__(self, element: T = None, nb_occurrences: int = None,\
         fils_gauche: Self = None, fils_droit: Self = None) -> None:
        self._element = element
        self._fils_gauche = fils_gauche
        self._fils_droit = fils_droit
        if (not (element is None) and not (nb_occurrences is None) \
            and fils_gauche is None and fils_droit is None):
            self._nb_occurrences = nb_occurrences
        elif (element is None and nb_occurrences is None and \
            not fils_gauche is None and not fils_droit is None):
            if fils_gauche is fils_droit:
                raise ArbreHuffmanIncoherentErreur("incoherent huffman tree")
            self._nb_occurrences = fils_gauche.nb_occurrences + fils_droit.nb_occurrences
        else:
            raise ArbreHuffmanIncoherentErreur("incoherent huffman tree")

    @property
    def est_une_feuille(self) -> bool:
        """permet de savoir si l'arbre est une feuille"""
        return self._fils_droit is None and self._fils_gauche is None

    @property
    def nb_occurrences(self) -> int:
        """permet d'obtenir le nombre d'occurence de la racine de l'arbre"""
        return self._nb_occurrences

    @property
    def element(self) -> T:
        """permet d'obtenir l'element d'une feuille"""
        if not self.est_une_feuille:
            raise DoitEtreUneFeuilleErreur("l'arbre doit être une feuille")
        return self._element

    @property
    def fils_gauche(self) -> Self:
        """permet d'obtenir le fils gauche d'un arbre"""
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("l'arbre doit pas être une feuille")
        return self._fils_gauche

    @property
    def fils_droit(self) -> Self:
        """permet d'obtenir le fils droit d'un arbre"""
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("l'arbre doit pas être une feuille")
        return self._fils_droit

    @property
    def hauteur(self) -> int:
        """permet d'obtenir la hauteur d'un arbre"""
        if self.est_une_feuille:
            return 0
        return max(self.fils_gauche.hauteur, self._fils_droit.hauteur) + 1

    def equivalent(self, autre: Self) -> bool:
        """retourne True lorsque deux arbres sont structurellement équivalents"""
        if self.est_une_feuille and autre.est_une_feuille:
            return self._element == autre.element and self._nb_occurrences == autre.nb_occurrences
        if not self.est_une_feuille and not autre.est_une_feuille:
            return self._fils_droit.equivalent(autre.fils_droit) \
                and self._fils_gauche.equivalent(autre.fils_gauche)
        return False

    def __eq__(self, autre) -> bool:
        """permet de tester si l'arbre est égal à un autre"""
        return self.equivalent(autre)

    def __lt__(self, autre) -> bool:
        """permet de tester si l'arbre est strictement inférieur à un autre"""
        return self._nb_occurrences < autre.nb_occurrences

    def __add__(self, autre) -> Self:
        """permet d'additionner deux arbres de huffman"""
        return ArbreHuffman(fils_gauche=self, fils_droit=autre)

    def __str__(self) -> str:
        def noeud_en_str(noeud: ArbreHuffman) -> str:
            if noeud.est_une_feuille:
                return f"({f"'{noeud.element}'"},{noeud.nb_occurrences})"
            return f"[{noeud.nb_occurrences}]"

        def rec_str(noeud: ArbreHuffman, prefix: str ="") -> str:
            if noeud is None:
                return ""
            result: str = noeud_en_str(noeud) + "\n"
            if not noeud.est_une_feuille:
                result += f"{prefix}|_{rec_str(noeud.fils_gauche, f"{prefix}|{2*" "}")}"
                result += f"{prefix}|_{rec_str(noeud.fils_droit, f"{prefix}{3*" "}")}"
            return result

        return rec_str(self)

    def fancy_str(self) -> str:
        """retourne une représentation humaine de l'arbre"""
        def arbre_ligne_par_ligne(arbre):
            """
            retourne une liste de chaine de caractère représentant 
            les lignes de l'arbre de la racine vers les feuilles
            """
            if arbre.est_une_feuille:
                ligne: str = f"({f"'{arbre.element}'":^4},{arbre.nb_occurrences:^5})"
                return [ligne], len(ligne), 1, len(ligne)//2
            gauche, largeur_gauche, hauteur_gauche, milieu_gauche = \
                arbre_ligne_par_ligne(arbre.fils_gauche)
            droite, largeur_droit, hauteur_droit, milieu_droit = \
                arbre_ligne_par_ligne(arbre.fils_droit)
            noeud = f"({arbre.nb_occurrences:^7})"
            ligne1 = ((milieu_gauche + 1) * ' ' )+((largeur_gauche - milieu_gauche - 1) * '_')+\
                          (noeud)+(milieu_droit * '_')+((largeur_droit - milieu_droit) * ' ')
            def connecteur(car1: str, car2: str) -> str:
                return (milieu_gauche * ' ')+(car1)+\
                       ((largeur_gauche - milieu_gauche - 1 + len(noeud) + milieu_droit) * ' ')+\
                       (car2)+((largeur_droit - milieu_droit - 1) * ' ')
            if hauteur_gauche < hauteur_droit:
                gauche += [largeur_gauche * ' '] * (hauteur_droit - hauteur_gauche)
            elif hauteur_droit < hauteur_gauche:
                droite += [largeur_droit * ' '] * (hauteur_gauche - hauteur_droit)
            lignes = [ligne1, connecteur('/', '\\'), connecteur('^', '^')] + \
                                [i + (len(noeud) * ' ') + j for i, j in zip(gauche, droite)]
            return lignes, (largeur_gauche + largeur_droit + len(noeud)), \
                   (max(hauteur_gauche, hauteur_droit) + 3), (largeur_gauche + len(noeud) // 2)

        lignes, *_ = arbre_ligne_par_ligne(self)
        return '\n'.join(lignes)

    def __repr__(self):
        """retourne une représentation formelle d'un arbre"""
        classe = 'ArbreHuffman'
        if self.est_une_feuille:
            return f"ArbreHuffman(element='{self._element}', nb_occurrences={self._nb_occurrences})"
        return f"{classe}(fils_gauche={repr(self.fils_gauche)},fils_droit={repr(self.fils_droit)})"


def main():
    """tests des fonctions repr et str"""
    a = ArbreHuffman(element='a', nb_occurrences=30)
    b = ArbreHuffman(element='b', nb_occurrences=134)
    c = ArbreHuffman(element='!', nb_occurrences=1)
    d = ArbreHuffman(element='d', nb_occurrences=54)
    e = ArbreHuffman(element='e', nb_occurrences=79)
    arbre = (a+(b+d))+(c+e)
    arbre2 = arbre + a
    arbre = arbre2 + (a+(c+b))
    print(f"__repr__ :\n\n{repr(arbre)}")
    print("")
    print(f"__str__ :\n\n{str(arbre)}")
    print("")
    print(f"fancy_str :\n\n{arbre.fancy_str()}")

if __name__ == "__main__":
    main()
