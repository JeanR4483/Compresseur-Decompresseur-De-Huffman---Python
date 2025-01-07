#!/usr/bin/env python3
""" Module proposant la classe Compteur """
from typing import TypeVar

T = TypeVar('T')

class Compteur:
    """ Compteur permet d'avoir des statistiques (nombre d'occurences) sur
des éléments hashables

    arguments:
    val_init -- dictionnaire(element, nb_occurences) qui permet d'initialiser
le compteur à sa création
    """
    def __init__(self, val_init: dict[T, int] = None):
# @u:start init

        self._occurences = {}
        if val_init is not None:
            self._occurences = dict(val_init.items())

# @u:end init

    def incrementer(self, element: T) -> None:
        """incremente de 1 le nb d'occurences de element

        arguments:
        element -- l'élément à incrémenter qui doit être hashable
        """
# @u:start incrementer
        self._occurences[element] = 1 if element not in self._occurences \
            else self._occurences[element] + 1

# @u:end incrementer

    def fixer(self, element: T, nb_occurences: int) -> None:
        """permet de fixer le nb d'occurences de element à valeur

        arguments:
        element -- l'élément hashable dont on veut fixer le nom d'occurences
        nb_occurences -- nombre d'occurences (>= 0) de l'élément
        """
# @u:start fixer
        self._occurences[element] = nb_occurences

# @u:end fixer

    def nb_occurrences(self, element: T) -> int:
        """permet d'obtenir le nb d'occurences de element

        arguments:
        element -- élément hashable dont on veut avoir le nombre d'occurences

        resultat: le nombre d'occurences, 0 si l'élément n'est pas présent
        """
# @u:start nb_occurences
        return 0 if element not in self._occurences else self._occurences[element]

# @u:end nb_occurences
    @property
    def elements(self) -> set[T]:
        """retourne tous les elements référencés

        resultat: un ensemble contenant les éléments référencés"""
# @u:start elements
        return self._occurences.keys()

# @u:end elements

    def _elements_ayant_un_nb_occurrences(self,
                                          selection_valeur=lambda l: l[0]):
        if not self._occurences.keys():
            return set()
        val = selection_valeur(self._occurences.values())
        return {el for el, nb in self._occurences.items() if nb == val}

    def elements_moins_frequents(self) -> set[T]:
        """retourne tous les elements les moins frequents

        resultat: un ensemble contenant les éléments les moins fréquents
        """
# @u:start elements_moins_frequents

        return self._elements_ayant_un_nb_occurrences(min)

# @u:end elements_moins_frequents

    def elements_plus_frequents(self) -> set[T]:
        """retourne tous les elements les plus frequents

        resultat: un ensemble contenant les éléments les plus fréquents
        """
# @u:start elements_plus_frequents

        return self._elements_ayant_un_nb_occurrences(max)

# @u:end elements_plus_frequents

    def elements_par_nb_occurrences(self) -> dict[int, set[T]]:
        """retourne pour chaque nombre d'occurences présents dans compteur
les éléments qui ont ces nombres d'occurences

        resultat: un dictionnaire dont les clés sont les nombres d'occurences
et les valeurs des ensembles d'éléments qui ont ce nombre d'occurences"""
# @u:start elements_par_nb_occurrences

        return {occ : self._elements_ayant_un_nb_occurrences(lambda l, o=occ : o) \
        	for occ in self._occurences.values()}

# @u:end elements_par_nb_occurrences

    def __repr__(self):
# @u:start repr

        return f"Compteur({self._occurences})"

# @u:end repr

    def __str__(self):
# @u:start str

        return f"{self._occurences}"

# @u:end str

    def __eq__(self, autre):
# @u:start eq

        return False if not isinstance(autre, self.__class__) \
                else self._occurences == autre._occurences

# @u:end eq

def main():
    """Tests unitaires du module"""
    def ok_ko_en_str(booleen):
        return "OK" if booleen else "KO"

    def ok_ko(fct, resultat_attendu, *param):
        """mini fonction de TU"""
        res = fct.__name__ + ' : '
        res = res + ok_ko_en_str(fct(*param) == resultat_attendu)
        print(res)

    cpt1 = Compteur()
    cpt1.incrementer('a')
    cpt1.incrementer('a')
    cpt1.incrementer('b')
    cpt1.incrementer('c')
    cpt1.incrementer('c')
    cpt1.incrementer('c')
    cpt1.incrementer('d')

    ok_ko(Compteur.nb_occurrences, 2, cpt1, 'a')
    ok_ko_en_str(cpt1.elements=={'a', 'b', 'c', 'd'})
    #ok_ko(Compteur.elements, {'a', 'b', 'c', 'd'}, cpt1)
    ok_ko(Compteur.elements_moins_frequents, {'b', 'd'}, cpt1)
    ok_ko(Compteur.elements_plus_frequents, {'c'}, cpt1)
    ok_ko(Compteur.elements_par_nb_occurrences, {1: {'b', 'd'}, 2: {'a'}, 3: {'c'}}, cpt1)
    ok_ko(str, "{'a': 2, 'b': 1, 'c': 3, 'd': 1}", cpt1)
    ok_ko(repr, "Compteur({'a': 2, 'b': 1, 'c': 3, 'd': 1})", cpt1)

    cpt2 = Compteur()
    cpt2.incrementer('c')
    cpt2.incrementer('c')
    cpt2.incrementer('c')
    cpt2.incrementer('d')
    cpt2.incrementer('a')
    cpt2.incrementer('a')
    cpt2.incrementer('b')
    print(f"égalité: {ok_ko_en_str(cpt1==cpt2)}")

if __name__ == "__main__":
    main()
