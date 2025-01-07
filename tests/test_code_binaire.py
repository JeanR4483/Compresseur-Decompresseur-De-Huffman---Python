#!/usr/bin/python3

import pytest
from huffman.code_binaire import CodeBinaire, Bit, AuMoinsUnBitErreur

@pytest.fixture(scope="function")    
def code_binaire():
    return CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)
    
def test_init_erreur():
    with pytest.raises(TypeError):
        CodeBinaire(1)

@pytest.mark.parametrize("cb1, cb2, resultat",
                         [(CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_0), True),
                          (CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_1), False),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_0, Bit.BIT_1), True),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_1, Bit.BIT_1), False),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_0), False)
                        ])
def test_eq(cb1, cb2, resultat):
    assert (cb1 == cb2) == resultat
    
def test_ajouter():
    code_binaire_un_bit = CodeBinaire(Bit.BIT_0)
    code_binaire_un_bit.ajouter(Bit.BIT_1)
    assert code_binaire_un_bit == CodeBinaire(Bit.BIT_0, Bit.BIT_1)
    
def test_ajouter_erreur(code_binaire):
    with pytest.raises(TypeError):
        code_binaire.ajouter(1)

@pytest.mark.parametrize("indice, resultat",
                        [(0, Bit.BIT_0),
                         (2, Bit.BIT_1),
                         (slice(0,2,None), CodeBinaire(Bit.BIT_0, Bit.BIT_1)),
                         (slice(1,4,None), CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)),
                         (slice(0,4,2), CodeBinaire(Bit.BIT_0, Bit.BIT_1))
                        ])
def test_getitem(code_binaire, indice, resultat):
    assert code_binaire[indice] == resultat
    
@pytest.mark.parametrize("indice, bit, resultat",
                        [(0, Bit.BIT_1, CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)),   # meme longeur
                         (1, Bit.BIT_0, CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)),   # meme longeur
                         (slice(0,2,None), CodeBinaire(Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)), # meme longueur
                         (slice(0,2,None), [Bit.BIT_1, Bit.BIT_0], CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)), # meme longueur
                         (slice(1,3,None), CodeBinaire(Bit.BIT_0, Bit.BIT_0), CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_0, Bit.BIT_0)), # meme longueur
                         (slice(0,4,2), CodeBinaire(Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)), # meme longueur
                         (slice(0,3,None), Bit.BIT_0, CodeBinaire(Bit.BIT_0, Bit.BIT_0)),               # raccourci
                         (slice(1,3,None), Bit.BIT_0, CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_0)),    # raccourci
                         (slice(1,3,None), [Bit.BIT_0], CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_0)),    # raccourci
                         (0, CodeBinaire(Bit.BIT_0, Bit.BIT_0), CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)), # allongé
                         (2, CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)), # allongé
                         (slice(1,3,None), CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)), # allongé
                         (slice(1,3,None), [Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0], CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)), # allongé
                         (slice(0,1,None), CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)) # allongé
                        ])
def test_setitem(code_binaire, indice, bit, resultat):
    code_binaire[indice] = bit
    assert code_binaire == resultat
    
@pytest.mark.parametrize("bit",
                        [(1),
                         (['a']),
                         ([Bit.BIT_1, Bit.BIT_0, 'aaa'])
                        ])
def test_setitem_erreur_typeerror(code_binaire, bit):
    with pytest.raises(TypeError):
        code_binaire[0] = bit
        
def test_setitem_erreur_aumoisunbiterreur(code_binaire):
    with pytest.raises(AuMoinsUnBitErreur):
        code_binaire[:] = []

@pytest.mark.parametrize("indice, resultat",
                        [(0, CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)),
                         (2, CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)),
                         (slice(0,2,None), CodeBinaire(Bit.BIT_1, Bit.BIT_0)),
                         (slice(1,4,None), CodeBinaire(Bit.BIT_0)),
                         (slice(0,4,2), CodeBinaire(Bit.BIT_1, Bit.BIT_0))
                        ])
def test_delitem(code_binaire, indice, resultat):
    del code_binaire[indice]
    assert code_binaire == resultat

@pytest.mark.parametrize("code, indice",
                        [(CodeBinaire(Bit.BIT_0), 0),
                         (CodeBinaire(Bit.BIT_0), slice(0,2,None)),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1), slice(0,2,None)),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1), slice(0,3,None))
                        ])
def test_delitem_erreur(code, indice):
    with pytest.raises(AuMoinsUnBitErreur):
        del code[indice]

@pytest.mark.parametrize("code1, code2, resultat",
                        [(CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_0, Bit.BIT_1)),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1)),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1), CodeBinaire(Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1, Bit.BIT_0))
                        ])
def test_add(code1, code2, resultat):
    assert (code1 + code2) == resultat
    
def test_add_erreur(code_binaire):
    with pytest.raises(TypeError):
        code_binaire + 1

@pytest.mark.parametrize("code, resultat",
                        [(CodeBinaire(Bit.BIT_0), 1),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1), 2),
                         (CodeBinaire(Bit.BIT_0, Bit.BIT_1) + CodeBinaire(Bit.BIT_1, Bit.BIT_0), 4),
                        ])
def test_len(code, resultat):
    assert len(code) == resultat
    
def test_len_cree_avec_ajouter():
    code = CodeBinaire(Bit.BIT_0, Bit.BIT_1)
    code.ajouter(Bit.BIT_0)
    assert len(code) == 3

def test_repr(code_binaire):
    assert eval(repr(code_binaire)) == code_binaire
    
def test_str(code_binaire):
    assert str(code_binaire) == "0110"
