#!/usr/bin/env python3
""" Module proposant la classe FileDePriorite """
from typing import TypeVar

T = TypeVar('T')

class FileDePriorite:
    """ FileDePriorite permet de représenter une file de priorite """

    def __init__(self, elements = (), cle: 'function' = lambda e:e) -> None:
        self._la_cle = cle
        self._file = []
        for elem in elements:
            self.enfiler(elem)

    @property
    def est_vide(self) -> bool:
        """ permet de savoir si la file st vide """
        return not self._file

    def _est_element_non_comparable(self, element_a_comparer: T) -> bool:
        autre = element_a_comparer if not self._file else self._file[0]
        try:
            _ = self._la_cle(element_a_comparer) <= self._la_cle(autre)
        except TypeError:
            return True
        return False

    def enfiler(self, element: T) -> None:
        """ permet d'enfiler une élément dans la file """
        if self._est_element_non_comparable(element):
            if not self._file:
                raise ElementNonComparableErreur\
                    (f"La classe de {element} ne possède pas les méthodes de comparaison")
            raise ElementNonComparableErreur\
                (f"{element} ne peut pas être comparé aux éléments de la file")
        i = 0
        while i < len(self._file) and  \
            self._la_cle(self._file[i]) <= self._la_cle(element):
            i += 1
        self._file.insert(i, element)

    @property
    def element(self) -> T:
        """ permet d'obtenir l'élément le plus prioritaire sans le défiler """
        if self.est_vide:
            raise FileDePrioriteVideErreur("la file de priorite est vide")
        return self._file[0]

    def defiler(self) -> T:
        """ permet de défiler l'élément le plus prioriaire, on obtient alors cet élément """
        if self.est_vide:
            raise FileDePrioriteVideErreur("la file de priorite est vide")
        return self._file.pop(0)

    def __len__(self) -> int:
        return len(self._file)

    def __iter__(self):
        yield from self._file

    def __repr__(self) -> str:
        return f"FileDePriorite({tuple(self._file)})"

    def __eq__(self, autre) -> bool:
        if not isinstance(autre, self.__class__):
            return False
        return self._file == autre._file

class FileDePrioriteVideErreur(Exception):
    """
    Exception levée lorsqu'on essaye d'obtenir ou défiler un élément en tête d'une file vide
    """

class ElementNonComparableErreur(Exception):
    """
    Exception levée lorsqu'on essaye d'ajouter un élément :
    - dont la classe ne possède pas les méthodes de comparaison
    - qui ne peut pas être comparée avec les éléments déjà présents dans la file
    """


def main():
    """ tests unitaire du module """
    def ok_ko_en_str(booleen):
        return "OK" if booleen else "KO"

    def ok_ko(fct, resultat_attendu, *param):
        """mini fonction de TU"""
        res = fct.__name__ + ' : '
        res = res + ok_ko_en_str(fct(*param) == resultat_attendu)
        print(res)

    file = FileDePriorite((1,3,4,9))
    file_vide = FileDePriorite()
    try:
        _ = file_vide.element
    except FileDePrioriteVideErreur:
        print("FileDePrioriteVideErreur : OK")
    try:
        _ = file_vide.defiler()
    except FileDePrioriteVideErreur:
        print("FileDePrioriteVideErreur : OK")
    try:
        file_vide.enfiler(complex(1,2))
    except ElementNonComparableErreur:
        print("ElementNonComparableErreur : OK")
    try:
        file.enfiler("zfee")
    except ElementNonComparableErreur:
        print("ElementNonComparableErreur : OK")
    print(f"repr : {repr(file)}")
    print(f"est_vide : {ok_ko_en_str(not file.est_vide)}")
    #ok_ko(FileDePriorite.est_vide, False, file)
    print(f"est_vide : {ok_ko_en_str(file_vide.est_vide)}")
    #ok_ko(FileDePriorite.est_vide, True, file_vide)
    print(f"element : {ok_ko_en_str(file.element == 1)}")
    #ok_ko(FileDePriorite.element, 1, file)
    ok_ko(FileDePriorite.defiler, 1, file)
    print(f"element : {ok_ko_en_str(file.element == 3)}")
    #ok_ko(FileDePriorite.element, 3, file)
    file.enfiler(2)
    #for elem in file:
    #    print(elem)s
    ok_ko(FileDePriorite.defiler, 2, file)


if __name__ == "__main__":
    main()
