from similarity_neo4j import SimilarityNeo4j, TermType
import pytest

SimilarityNeo4j.init_driver()


@pytest.mark.asyncio
async def test_check_term():
    similarity_neo4j = SimilarityNeo4j()

    assert similarity_neo4j.check_term('HP:0000001', TermType.HPO)

    assert not similarity_neo4j.check_term('Invalid Test Term:0000001', TermType.HPO)

    assert similarity_neo4j.check_term('ORPHA:12345', TermType.ORDO)

    assert not similarity_neo4j.check_term('ORPHA:ABCDE', TermType.ORDO)


@pytest.mark.parametrize("terms, term_type", [(['HP:0000001', 'HP:0000002'], TermType.HPO),
                                              (['ORPHA:12345', 'ORPHA:12346'], TermType.ORDO)
                                              ])
def test_check_terms_valid(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type)[0] is True


@pytest.mark.parametrize("terms, term_type", [(['HP:0000001', 'InvalidTerm'], TermType.HPO),
                                              (['ORPHA:12345', 'Wrong:12346'], TermType.ORDO)
                                              ])
def test_check_terms_with_invalid(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type) is False


@pytest.mark.parametrize("terms, term_type", [(['Invalid1', 'Invalid2'], TermType.HPO),
                                              (['Wrong1', 'Wrong2'], TermType.ORDO)
                                              ])
def test_check_terms_all_invalid(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type) is False


@pytest.mark.parametrize("terms, term_type", [(['HP:0000001', 'HP:0000002'], TermType.HPO),
                                              (['ORPHA:12345', 'ORPHA:12346'], TermType.ORDO)
                                              ])
def test_check_terms_valid_raise(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type, will_raise=True)[0] is True


@pytest.mark.parametrize("terms, term_type", [(['HP:0000001', 'InvalidTerm'], TermType.HPO),
                                              (['ORPHA:12345', 'Wrong:12346'], TermType.ORDO)
                                              ])
def test_check_terms_with_invalid_raise(terms, term_type):
    with pytest.raises(ValueError):
        SimilarityNeo4j.check_terms(terms, term_type, will_raise=True)


@pytest.mark.asyncio
async def test_check_term_for_different_types():
    similarity_neo4j = SimilarityNeo4j()

    assert similarity_neo4j.check_term('OMIM:123456', TermType.OMIM)
    assert not similarity_neo4j.check_term('OMIM:ABCDEF', TermType.OMIM)

    assert similarity_neo4j.check_term('R-HSA-1234567', TermType.PATHWAY)
    assert not similarity_neo4j.check_term('R-HSA-ABCDEFG', TermType.PATHWAY)

    assert similarity_neo4j.check_term('R-HSA-1234567', TermType.REACTION)
    assert not similarity_neo4j.check_term('R-HSA-ABCDEFG', TermType.REACTION)


@pytest.mark.parametrize("terms, term_type", [
    (['OMIM:123456', 'OMIM:123457'], TermType.OMIM),
    (['R-HSA-1234567', 'R-HSA-7654321'], TermType.PATHWAY),
    (['R-HSA-2345678', 'R-HSA-8765432'], TermType.REACTION),
])
def test_check_terms_valid_other_types(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type)[0] is True


@pytest.mark.parametrize("terms, term_type", [
    (["APOC2", "APOA1"], TermType.GENE),
    (["APOE_intergenic_variant", "APOE_splice_region_variant"], TermType.PROTEIN_EFFECT),
])
def test_check_terms_valid_other_types_gene(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type) is False


@pytest.mark.parametrize("terms, term_type", [
    (['OMIM:123456', 'InvalidTerm'], TermType.OMIM),
    (['R-HSA-1234567', 'InvalidTerm'], TermType.PATHWAY),
    (['R-HSA-2345678', 'InvalidTerm'], TermType.REACTION),
])
def test_check_terms_with_some_invalid_other_types(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type) is False


@pytest.mark.parametrize("terms, term_type", [
    (['Invalid1', 'Invalid2'], TermType.OMIM),
    (['InvalidPathway1', 'InvalidPathway2'], TermType.PATHWAY),
    (['InvalidReaction1', 'InvalidReaction2'], TermType.REACTION),
])
def test_check_terms_all_invalid_other_types(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type) is False


@pytest.mark.parametrize("terms, term_type", [
    (['OMIM:123456', 'OMIM:123457'], TermType.OMIM),
    (['R-HSA-1234567', 'R-HSA-7654321'], TermType.PATHWAY),
    (['R-HSA-2345678', 'R-HSA-8765432'], TermType.REACTION),
])
def test_check_terms_valid_raise_other_types(terms, term_type):
    assert SimilarityNeo4j.check_terms(terms, term_type, will_raise=True)[0] is True


@pytest.mark.parametrize("terms, term_type", [
    (['OMIM:123456', 'InvalidTerm'], TermType.OMIM),
    (['R-HSA-1234567', 'InvalidPathwayTerm'], TermType.PATHWAY),
    (['R-HSA-2345678', 'InvalidReactionTerm'], TermType.REACTION),
])
def test_check_terms_with_some_invalid_raise_other_types(terms, term_type):
    with pytest.raises(ValueError):
        SimilarityNeo4j.check_terms(terms, term_type, will_raise=True)


