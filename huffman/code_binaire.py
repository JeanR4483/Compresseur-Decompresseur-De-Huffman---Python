#!/usr/bin/env python3
""" Module proposant une implémentation du type Bit et de la classe CodeBinaire """
from enum import Enum
from typing import Self

class Bit(Enum):
    """ Type Bit """
    BIT_0 = 0
    BIT_1 = 1

class CodeBinaire():
    """ Code Binaire """

    def __init__(self, bit: Bit, *bits: Bit) -> None:
        """
        initialise le code binaire
        """
        if not isinstance(bit, Bit):
            raise TypeError("le code binaire doit être construit à partir de Bit")
        self._les_bits = [bit]
        for bit in bits:
            self.ajouter(bit)

    def ajouter(self, bit: Bit) -> None:
        """
        ajoute un bit à la fin du code binaire
        """
        if not isinstance(bit, Bit):
            raise TypeError("le code binaire doit être construit à partir de Bit")
        self._les_bits.append(bit)

    def __len__(self):
        """
        renvoie la longueur du code binaire
        """
        return len(self._les_bits)

    def __getitem__(self, indice_du_slice: int|slice) -> Bit|Self:
        """
        obtenir un bit du code binaire
        """
        if isinstance(indice_du_slice, int):
            return self._les_bits[indice_du_slice]
        return CodeBinaire(*self._les_bits[indice_du_slice])

    def __setitem__(self, indice_du_slice: int|slice, bit: Bit) -> None:
        """
        Modifie une partie du code binaire
        """
        if isinstance(indice_du_slice, int):
            if isinstance(bit, CodeBinaire):
                self._les_bits[indice_du_slice:indice_du_slice+1] = bit._les_bits
            elif isinstance(bit, Bit):
                self._les_bits[indice_du_slice] = bit
            elif isinstance(bit, list):
                if not bit:
                    raise AuMoinsUnBitErreur("Un code binaire doit posséder au moins un bit")
                for iemebit in bit:
                    if not isinstance(iemebit, Bit):
                        raise TypeError("Le code binaire doit être construit à partir de Bit")
                    self._les_bits[indice_du_slice:indice_du_slice+1] = bit
            else:
                raise TypeError("Le code binaire doit être construit à partir de Bit")
            return

        if isinstance(bit, CodeBinaire):
            self._les_bits[indice_du_slice] = bit._les_bits
        elif isinstance(bit, Bit):
            self._les_bits[indice_du_slice] = [bit]
        elif isinstance(bit, list):
            if not bit:
                raise AuMoinsUnBitErreur("Un code binaire doit posséder au moins un bit")
            for iemebit in bit:
                if not isinstance(iemebit, Bit):
                    raise TypeError("Le code binaire doit être construit à partir de Bit")
            self._les_bits[indice_du_slice] = bit
        else:
            raise TypeError("Le code binaire doit être construit à partir de Bit")
        return

    def _slice_trop_long(self, le_slice : slice) -> bool:
        """
        vérifie si un slice est plus long qu'un code binaire
        """
        if le_slice.step is None:
            return len(self._les_bits) <= (le_slice.stop - le_slice.start)
        return len(self._les_bits) <= ((le_slice.stop - 1 - le_slice.start) // le_slice.step)

    def __delitem__(self, indice_du_slice: int|slice) -> None:
        """
        supprime un bit
        """
        if (isinstance(indice_du_slice, int) and len(self._les_bits) <= 1)\
            or (isinstance(indice_du_slice, slice) and self._slice_trop_long(indice_du_slice)):
            raise AuMoinsUnBitErreur("Un code binaire doit posséder au moins un bit")
        del self._les_bits[indice_du_slice]

    def __add__(self, autre : Self) -> Self:
        """
        additionne deux codes binaires entre eux
        """
        if not isinstance(autre, CodeBinaire):
            raise TypeError("Le code binaire doit être construit à partir de Bit")
        return CodeBinaire(*(self._les_bits + autre._les_bits))

    def __iter__(self):
        """
        itere sur les elements
        """
        yield from self._les_bits

    def __eq__(self, autre:"CodeBinaire"):
        """
        teste l'égalité entre deux codes binaires
        """
        if not isinstance(autre, CodeBinaire):
            return False
        return self._les_bits == autre._les_bits

    def __repr__(self):
        """
        representaion formelle du code binaire
        """
        return f"CodeBinaire({", ".join(f"{bit}" for bit in self._les_bits)})"

    def __str__(self):
        """
        representaion informelle du code binaire
        """
        return "".join([str(bit.value) for bit in self._les_bits])


    def __hash__(self):
        return 7*hash(self._les_bits)

class AuMoinsUnBitErreur(Exception):
    """
    Exception levée lorsque l'on supprime un nombre de bit qui aboutirait \
        à avoir au moins un code binaire sans bit.
    """


def tests_exceptions():
    """
    Test des exceptions
    """
    try:
        _ = CodeBinaire(1)
        print("TypeError : KO")
    except TypeError:
        print("TypeError : OK")

    try:
        code_binaire = CodeBinaire(Bit.BIT_0)
        code_binaire.ajouter(1)
        print("TypeError : KO")
    except TypeError:
        print("TypeError : OK")

    try:
        c_erreur = CodeBinaire(Bit.BIT_0)
        del c_erreur[0]
        print("AuMoinsUnBitErreur : KO")
    except AuMoinsUnBitErreur:
        print("AuMoinsUnBitErreur : OK")

    try:
        c_erreur2 = CodeBinaire(Bit.BIT_0, Bit.BIT_1)
        del c_erreur2[0:2]
        print("AuMoinsUnBitErreur : KO")
    except AuMoinsUnBitErreur:
        print("AuMoinsUnBitErreur : OK")

def main():
    """Tests unitaires du module"""
    def ok_ko_en_str(booleen):
        return "OK" if booleen else "KO"

    def ok_ko(fct, resultat_attendu, *param):
        """mini fonction de TU"""
        res = fct.__name__ + ' : '
        res = res + ok_ko_en_str(fct(*param) == resultat_attendu)
        print(res)

    code_binaire = CodeBinaire(Bit.BIT_0, Bit.BIT_1)
    ok_ko(len, 2, code_binaire)
    print()

    ok_ko(CodeBinaire.__eq__, False, code_binaire, CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1))
    ok_ko(CodeBinaire.__eq__, True, code_binaire, CodeBinaire(Bit.BIT_0, Bit.BIT_1))
    print()

    code_binaire.ajouter(Bit.BIT_1)
    print(f"__getitem__ : {ok_ko_en_str(code_binaire[0] == Bit.BIT_0)}")
    print(f"__getitem__ : {ok_ko_en_str(code_binaire[2] == Bit.BIT_1)}")
    print(f"__getitem__ : {ok_ko_en_str(code_binaire[1:3] == CodeBinaire(Bit.BIT_1, Bit.BIT_1))}")
    print()

    code_binaire[1] = Bit.BIT_0
    test_setitem_1 = ok_ko_en_str(code_binaire == CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1))
    print(f"__setitem__ : {test_setitem_1}")
    code_binaire[0:2] = CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)
    test_setitem_2 = \
        ok_ko_en_str(code_binaire == CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0, Bit.BIT_1))
    print(f"__setitem__ : {test_setitem_2}")
    code_binaire[0:2] = Bit.BIT_1
    test_setitem_3 = ok_ko_en_str(code_binaire == CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_1))
    print(f"__setitem__ : {test_setitem_3}")
    print()

    code_binaire2 = \
        CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0, Bit.BIT_1, Bit.BIT_0, Bit.BIT_1)
    del code_binaire2[3]
    test_delitem_1 = ok_ko_en_str(code_binaire2 == \
                    CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0, Bit.BIT_0, Bit.BIT_1))
    print(f"__delitem__ : {test_delitem_1}")
    del code_binaire2[1:4]
    test_delitem_2 = ok_ko_en_str(code_binaire2 == CodeBinaire(Bit.BIT_1, Bit.BIT_1))
    print(f"__delitem__ : {test_delitem_2}")
    print()

    print(f"str : {str(code_binaire)}\n")
    print(f"repr : {repr(code_binaire)}\n")

    tests_exceptions()

if __name__ == "__main__":
    main()
