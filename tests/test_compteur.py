#!/usr/bin/python3

import pytest
from huffman.compteur import Compteur

@pytest.fixture(scope="function")
def compteur_vide():
    return Compteur()

@pytest.fixture(scope="function")
def compteur_non_vide():
    return Compteur({'a':2,'b':1,'c':3,'d':1})


def test_nb_occurences_present(compteur_non_vide):
    assert compteur_non_vide.nb_occurrences('a') == 2

def test_nb_occurences_non_present(compteur_non_vide):
    assert compteur_non_vide.nb_occurrences('z') == 0

def test_incrementer_present(compteur_non_vide):
    compteur_non_vide.incrementer('a')
    assert compteur_non_vide.nb_occurrences('a') == 3

def test_incrementer_non_present(compteur_non_vide):
    compteur_non_vide.incrementer('z')
    assert compteur_non_vide.nb_occurrences('z') == 1

def test_fixer_present(compteur_non_vide):
    compteur_non_vide.fixer('a', 5)
    assert compteur_non_vide.nb_occurrences('a') == 5

def test_fixer_non_present(compteur_non_vide):
    compteur_non_vide.fixer('z', 5)
    assert compteur_non_vide.nb_occurrences('z') == 5

def test_elements_compteur_vide(compteur_vide):
    assert compteur_vide.elements == set()

def test_elements_compteur_non_vide(compteur_non_vide):
    assert set(compteur_non_vide.elements) == {"a","b","c","d"}

@pytest.mark.parametrize("compteur, elements",
                         [(Compteur(), set()),
                          (Compteur({'a':2,'b':1,'c':3,'d':1}), {"b","d"})
                        ])
def test_elements_moins_frequents(compteur, elements):
    assert compteur.elements_moins_frequents() == elements

@pytest.mark.parametrize("compteur, elements",
                         [(Compteur(), set()),
                          (Compteur({'a':2,'b':1,'c':3,'d':1}), {"c"})
                        ])
def test_elements_plus_frequents(compteur, elements):
    assert compteur.elements_plus_frequents() == elements

def test_elements_par_nb_occurences(compteur_non_vide):
    assert compteur_non_vide.elements_par_nb_occurrences() == {1: {'b','d'}, 2:{'a'}, 3:{'c'}}

@pytest.mark.parametrize("compteur",
                         [(Compteur()),
                          (Compteur({'a':2,'b':1,'c':3,'d':1}))
                        ])
def test_repr(compteur):
    assert eval(repr(compteur)) == compteur
