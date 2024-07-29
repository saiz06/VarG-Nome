from similarity_neo4j import frequency_to_string
import pytest


def test_frequency_zero():
    assert frequency_to_string(0) == [
        'Excluded (0%)',
        'Very rare (<4-1%)',
        'Occasional (29-5%)',
        'Frequent (79-30%)',
        'Very frequent (99-80%)',
        'Obligate (100%)',
    ]


def test_frequency_very_rare():
    assert frequency_to_string(4) == [
        'Very rare (<4-1%)',
        'Occasional (29-5%)',
        'Frequent (79-30%)',
        'Very frequent (99-80%)',
        'Obligate (100%)',
    ]


def test_frequency_occasional():
    assert frequency_to_string(29) == [
        'Occasional (29-5%)',
        'Frequent (79-30%)',
        'Very frequent (99-80%)',
        'Obligate (100%)',
    ]


def test_frequency_frequent():
    assert frequency_to_string(79) == [
        'Frequent (79-30%)',
        'Very frequent (99-80%)',
        'Obligate (100%)',
    ]


def test_frequency_very_frequent():
    assert frequency_to_string(99) == [
        'Very frequent (99-80%)',
        'Obligate (100%)',
    ]


def test_frequency_obligate():
    assert frequency_to_string(100) == ['Obligate (100%)']


def test_negative_frequency():
    with pytest.raises(ValueError):
        frequency_to_string(-1)


def test_frequency_over_100():
    with pytest.raises(ValueError):
        frequency_to_string(101)
