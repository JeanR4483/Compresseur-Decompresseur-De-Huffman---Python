#!/usr/bin/python3

import pytest
from huffman.file_de_priorite import FileDePriorite, FileDePrioriteVideErreur, ElementNonComparableErreur
import copy

@pytest.fixture(scope="function")
def file_vide():
    return FileDePriorite()

@pytest.fixture(scope="function")
def file_non_vide():
    return FileDePriorite((2,1,4,3,5))

@pytest.fixture(scope="function")
def file_non_vide2():
    return FileDePriorite((2,1,4,3,5))

@pytest.mark.parametrize("file_d_p, resultat",
                         [(FileDePriorite(), True),
                          (FileDePriorite((2,1,4,3,5)), False)
                        ])
def test_est_vide(file_d_p, resultat):
    assert file_d_p.est_vide == resultat

@pytest.mark.parametrize("file_d_p1, file_d_p2, resultat",
                         [(FileDePriorite(), FileDePriorite(), True),
                          (FileDePriorite(), FileDePriorite((2,1,4,3,5)), False),
                          (FileDePriorite((2,1,4,3,5)), FileDePriorite((2,1,4,3,5)), True)
                        ])    
def test_eq(file_d_p1, file_d_p2, resultat):
    assert (file_d_p1 == file_d_p2) == resultat

def test_enfiler_defiler_plus_prioritaire(file_non_vide, file_non_vide2):
    file_non_vide2.enfiler(0)
    file_non_vide2.defiler()
    assert file_non_vide2 == file_non_vide

def test_enfiler_defiler_non_prioritaire(file_non_vide, file_non_vide2):
    file_non_vide2.enfiler(4)
    file_non_vide2.defiler()
    assert file_non_vide2 == FileDePriorite((2,4,4,3,5))
    
def test_enfiler_element_plus_prioritaire(file_non_vide, file_non_vide2):
    file_non_vide2.enfiler(0)
    assert file_non_vide2.element == 0

@pytest.mark.parametrize("file_d_p",
                         [(FileDePriorite()),
                          (FileDePriorite((2,1,4,3,5)))
                        ])     
def test_repr(file_d_p):
    eval(repr(file_d_p)) == file_d_p

def test_vide_erreur(file_vide):
    with pytest.raises(FileDePrioriteVideErreur):
        file_vide.element
    
def test_non_comparable_erreur(file_non_vide):
    with pytest.raises(ElementNonComparableErreur):
        file_non_vide.enfiler("a")
