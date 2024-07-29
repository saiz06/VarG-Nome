from unittest.mock import AsyncMock, MagicMock, patch
from similarity_neo4j import SimilarityNeo4j
import pytest

SimilarityNeo4j.init_driver()


@pytest.mark.asyncio
async def test_execute_query():
    mock_run_method = AsyncMock(return_value=MagicMock(data=AsyncMock(return_value=["HP:0007020", "HP:0001258"])))

    mock_session = AsyncMock(run=mock_run_method)

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j.driver, 'session',
                      return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session),
                                             __aexit__=AsyncMock(return_value=None))):
        result = await similarity_neo4j.execute_query('m_query', {'hpo_term': "HP:0001258", 'depth': 3})

        mock_run_method.assert_called_with('m_query', {'hpo_term': "HP:0001258", 'depth': 3})

        assert result == ["HP:0007020", "HP:0001258"]


@pytest.mark.asyncio
async def test_hpo_expand_single_depth_three():
    mock_execute_query = AsyncMock(return_value=[{"children": ["HP:0001259", "HP:0001260"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_expand_single("HP:0001258", 3)

        expected_query = """
        MATCH (n:HPOterm)<-[:IS_A*0..3]-(m:HPOterm)
        WHERE n.hpoid = $hpoid
        RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
        """
        expected_parameters = {'hpoid': "HP:0001258"}

        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)
        assert result == [{"children": ["HP:0001259", "HP:0001260"]}]


@pytest.mark.asyncio
async def test_hpo_expand_single_depth_five():
    mock_execute_query = AsyncMock(
        return_value=[{"children": ["HP:0002179", "HP:0002510", "HP:0002491", "HP:0012407", "HP:0031958", "HP:0031957",
                                    "HP:0002064", "HP:0001264", "HP:0011099", "HP:0002464", "HP:0007020", "HP:0001258",
                                    "HP:0007199", "HP:0002313", "HP:0002061", "HP:0001285", "HP:0002501", "HP:0006986",
                                    "HP:0006983", "HP:0002478", "HP:0002191", "HP:0031866", "HP:0001257"]}])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_expand_single("HP:0001258", 5)

        expected_query = """
        MATCH (n:HPOterm)<-[:IS_A*0..5]-(m:HPOterm)
        WHERE n.hpoid = $hpoid
        RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
        """
        expected_parameters = {'hpoid': "HP:0001258"}

        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)
        assert result == [
            {"children": ["HP:0002179", "HP:0002510", "HP:0002491", "HP:0012407", "HP:0031958", "HP:0031957",
                          "HP:0002064", "HP:0001264", "HP:0011099", "HP:0002464", "HP:0007020", "HP:0001258",
                          "HP:0007199", "HP:0002313", "HP:0002061", "HP:0001285", "HP:0002501", "HP:0006986",
                          "HP:0006983", "HP:0002478", "HP:0002191", "HP:0031866", "HP:0001257"]}]


@pytest.mark.asyncio
async def test_hpo_expand_single_depth_zero():
    mock_execute_query = AsyncMock(return_value=[{"children": ["HP:0001257"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_expand_single("HP:0001258", 0)

        assert result == [{"children": ["HP:0001257"]}]


@pytest.mark.asyncio
async def test_hpo_expand_multiple_depth_three():
    mock_execute_query = AsyncMock(return_value=[{"children": ["HP:0001259", "HP:0001260", "HP:0001261"]}])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_expand_multiple(["HP:0001258", "HP:0001257"], 3)

        expected_query = """
        MATCH (n:HPOterm)<-[:IS_A*0..3]-(m:HPOterm)
        WHERE n.hpoid IN $hpoids
        RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
        """
        expected_parameters = {'hpoids': ["HP:0001258", "HP:0001257"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{"children": ["HP:0001259", "HP:0001260", "HP:0001261"]}]


@pytest.mark.asyncio
async def test_hpo_expand_multiple_depth_zero():
    mock_execute_query = AsyncMock(return_value=[{"children": ["HP:0000001"]}])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_expand_multiple(["HP:0000001"], 0)

        expected_query = """
        MATCH (n:HPOterm)<-[:IS_A*0..]-(m:HPOterm)
        WHERE n.hpoid IN $hpoids
        RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
        """
        expected_parameters = {'hpoids': ["HP:0000001"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{"children": ["HP:0000001"]}]


@pytest.mark.asyncio
async def test_hpo_similarity_query_multiple_terms_default_threshold():
    mock_execute_query = AsyncMock(return_value=[{"id": "HP:0000002", "similarIDs": ["HP:0004322"]}])
    similarity_neo4j = SimilarityNeo4j()
    hpo_terms = ["HP:0000002"]

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.hpo_similarity_query(hpo_terms)

        assert result == [{"id": "HP:0000002", "similarIDs": ["HP:0004322"]}]

