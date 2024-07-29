from unittest.mock import AsyncMock, MagicMock, patch
from similarity_neo4j import SimilarityNeo4j
import pytest

SimilarityNeo4j.init_driver()


@pytest.mark.asyncio
async def test_map_hpo_ordo_multiple_terms_default_params():
    mock_execute_query = AsyncMock(return_value=[{"hpoID": "HP:0000002", "orphaIDs": ["ORPHA:432", "ORPHA:140976"]}])
    similarity_neo4j = SimilarityNeo4j()
    hpo_terms = ["HP:0000001", "HP:0000002"]

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_hpo_ordo(hpo_terms, frequency=3)

        assert result == [{"hpoID": "HP:0000002", "orphaIDs": ["ORPHA:432", "ORPHA:140976"]}]


@pytest.mark.asyncio
async def test_map_pathway_reaction():
    mock_execute_query = AsyncMock(return_value=[{'reactionIDs': ['R-HSA-8852280', 'R-HSA-8852306', 'R-HSA-8852351', 'R-HSA-8852324',
                                                                  'R-HSA-8852317', 'R-HSA-8852362', 'R-HSA-8852331', 'R-HSA-8852337',
                                                                  'R-HSA-8852298', 'R-HSA-8852354']}])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_pathway_reaction(["R-HSA-8852276"])
        expected_query = """
        MATCH (n:Pathway)<-[:PART_OF_PATHWAY]-(n1:Reaction)
        WHERE n.ReactomePathwayID IN $pathwayids
        RETURN DISTINCT(n.ReactomePathwayID) AS pathwayID, collect(DISTINCT(n1.ReactomeReactionID)) AS reactionIDs;
        """
        expected_parameters = {'pathwayids': ["R-HSA-8852276"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{'reactionIDs': ['R-HSA-8852280', 'R-HSA-8852306', 'R-HSA-8852351', 'R-HSA-8852324', 'R-HSA-8852317',
                                           'R-HSA-8852362', 'R-HSA-8852331', 'R-HSA-8852337', 'R-HSA-8852298', 'R-HSA-8852354']}]


@pytest.mark.asyncio
async def test_map_reaction_pathway():
    mock_execute_query = AsyncMock(return_value=[{'pathwayIDs': ["R-HSA-168249", "R-HSA-168898", "R-HSA-168256", "R-HSA-5686938"]}])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_reaction_pathway(["R-HSA-8869667"])
        expected_query = """
        MATCH (n:Reaction)-[:PART_OF_PATHWAY]->(n1:Pathway)
        WHERE n.ReactomeReactionID IN $reactionids
        RETURN DISTINCT(n.ReactomeReactionID) AS reactionID, COLLECT(DISTINCT(n1.ReactomePathwayID)) AS pathwayIDs;
        """

        expected_parameters = {'reactionids': ["R-HSA-8869667"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{'pathwayIDs': ["R-HSA-168249", "R-HSA-168898", "R-HSA-168256", "R-HSA-5686938"]}]


@pytest.mark.asyncio
async def test_map_gene_reaction():
    mock_execute_query = AsyncMock(return_value=[{'reactionIDs': ['R-HSA-266303', 'R-HSA-174757', 'R-HSA-2404140', 'R-HSA-174690',
                                                                  'R-HSA-174657', 'R-HSA-9612243', 'R-HSA-8869590', 'R-HSA-174808',
                                                                  'R-HSA-174624', 'R-HSA-174706', 'R-HSA-2395768', 'R-HSA-9031512',
                                                                  'R-HSA-8952289', 'R-HSA-2424254', 'R-HSA-2507854', 'R-HSA-174660',
                                                                  'R-HSA-2173778', 'R-HSA-2423785', 'R-HSA-2429643', 'R-HSA-174739',
                                                                  'R-HSA-2395784', 'R-HSA-2404131']}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_gene_reaction(["APOE"])

        expected_query = """
        MATCH (n:Gene)<-[:USING_GENE_PRODUCT]-(n1:Reaction)
        WHERE n.Symbol IN $symbols
        RETURN DISTINCT(n.Symbol) AS symbol, COLLECT(DISTINCT(n1.ReactomeReactionID)) AS reactionIDs;
        """

        expected_parameters = {'symbols': ["APOE"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{'reactionIDs': ['R-HSA-266303', 'R-HSA-174757', 'R-HSA-2404140', 'R-HSA-174690', 'R-HSA-174657',
                                           'R-HSA-9612243', 'R-HSA-8869590', 'R-HSA-174808', 'R-HSA-174624', 'R-HSA-174706',
                                           'R-HSA-2395768', 'R-HSA-9031512', 'R-HSA-8952289', 'R-HSA-2424254', 'R-HSA-2507854',
                                           'R-HSA-174660', 'R-HSA-2173778', 'R-HSA-2423785', 'R-HSA-2429643', 'R-HSA-174739',
                                           'R-HSA-2395784', 'R-HSA-2404131']}]


@pytest.mark.asyncio
async def test_map_gene_reaction():
    mock_execute_query = AsyncMock(return_value=[{'symbols': ["APOC2", "APOA1", "APOC3", "APOE"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_reaction_gene(["R-HSA-266303"])

        expected_query = """
        MATCH (n:Reaction)-[:USING_GENE_PRODUCT]->(n1:Gene)
        WHERE n.ReactomeReactionID IN $reactionids
        RETURN DISTINCT(n.ReactomeReactionID) AS reactionID, COLLECT(DISTINCT(n1.Symbol)) AS symbols;
        """

        expected_parameters = {'reactionids': ["R-HSA-266303"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{'symbols': ["APOC2", "APOA1", "APOC3", "APOE"]}]


@pytest.mark.asyncio
async def test_map_gene_protein():
    mock_execute_query = AsyncMock(
        return_value=[{'proteinEffects': ["APOE_intergenic_variant", "APOE_splice_region_variant", "APOE_start_retained_variant",
                                          "APOE_NMD_transcript_variant", "APOE_three_prime_UTR_variant", "APOE_downstream_gene_variant",
                                          "APOE_upstream_gene_variant", "APOE_inframe_insertion", "APOE_non_coding_transcript_variant",
                                          "APOE_stop_retained_variant", "APOE_frameshift_variant", "APOE_splice_acceptor_variant", "APOE_start_lost",
                                          "APOE_intron_variant", "APOE_stop_lost", "APOE_non_coding_transcript_exon_variant", "APOE_synonymous_variant",
                                          "APOE_coding_sequence_variant", "APOE_splice_donor_variant", "APOE_five_prime_UTR_variant", "APOE_missense_variant",
                                          "APOE_stop_gained", "APOE_inframe_deletion"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_gene_protein(["APOE"])

        expected_query = """
        MATCH (n:Gene)-[:HAS_EFFECT]->(n1:Protein_Effect)
        WHERE n.Symbol IN $symbols
        RETURN DISTINCT(n.Symbol) AS symbol, COLLECT(DISTINCT(n1.type)) AS proteinEffects;
        """

        expected_parameters = {'symbols': ["APOE"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [
            {'proteinEffects': ["APOE_intergenic_variant", "APOE_splice_region_variant", "APOE_start_retained_variant", "APOE_NMD_transcript_variant",
                                "APOE_three_prime_UTR_variant", "APOE_downstream_gene_variant", "APOE_upstream_gene_variant", "APOE_inframe_insertion",
                                "APOE_non_coding_transcript_variant", "APOE_stop_retained_variant", "APOE_frameshift_variant", "APOE_splice_acceptor_variant",
                                "APOE_start_lost", "APOE_intron_variant", "APOE_stop_lost", "APOE_non_coding_transcript_exon_variant", "APOE_synonymous_variant",
                                "APOE_coding_sequence_variant", "APOE_splice_donor_variant", "APOE_five_prime_UTR_variant", "APOE_missense_variant", "APOE_stop_gained",
                                "APOE_inframe_deletion"]}]


@pytest.mark.asyncio
async def test_map_protein_gene():
    mock_execute_query = AsyncMock(return_value=[{'symbols': ["APOE"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.map_protein_gene(["APOE"])

        expected_query = """
        MATCH (n:Protein_Effect)<-[:HAS_EFFECT]-(n1:Gene)
        WHERE n.type IN $proteinEffects
        RETURN DISTINCT(n.type) AS variant, COLLECT(DISTINCT(n1.Symbol)) AS symbols;
        """

        expected_parameters = {'proteinEffects': ["APOE"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{'symbols': ["APOE"]}]
