from unittest.mock import AsyncMock, patch
from similarity_neo4j import SimilarityNeo4j
import pytest

SimilarityNeo4j.init_driver()


@pytest.mark.asyncio
async def test_ordo_expand_single_depth_three():
    mock_execute_query = AsyncMock(return_value=[{"children": ["ORPHA:0001259", "ORPHA:0001260"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.ordo_expand_single("ORPHA:0001258", 3)

        expected_query = """
        MATCH (n:ORPHAterm)<-[:IS_A*0..3]-(m:ORPHAterm)
        WHERE n.orphaid = $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """
        expected_parameters = {'orphaid': "ORPHA:0001258"}

        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)
        assert result == [{"children": ["ORPHA:0001259", "ORPHA:0001260"]}]


@pytest.mark.asyncio
async def test_ordo_expand_single_depth_five():
    mock_execute_query = AsyncMock(return_value=[{"children": ["ORPHA:0001259", "ORPHA:0001260"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.ordo_expand_single("ORPHA:0001258", 5)

        expected_query = """
        MATCH (n:ORPHAterm)<-[:IS_A*0..5]-(m:ORPHAterm)
        WHERE n.orphaid = $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """
        expected_parameters = {'orphaid': "ORPHA:0001258"}

        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)
        assert result == [{"children": ["ORPHA:0001259", "ORPHA:0001260"]}]


@pytest.mark.asyncio
async def test_ordo_expand_single_depth_zero():
    mock_execute_query = AsyncMock(return_value=[{"children": ["ORPHA:377792"]}])
    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.ordo_expand_single("ORPHA:377792", 0)

        expected_query = """
        MATCH (n:ORPHAterm)<-[:IS_A*0..]-(m:ORPHAterm)
        WHERE n.orphaid = $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """

        expected_parameters = {'orphaid': "ORPHA:377792"}

        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)
        assert result == [{"children": ["ORPHA:377792"]}]


@pytest.mark.asyncio
async def test_ordo_expand_multiple_depth_three():
    mock_execute_query = AsyncMock(return_value=[
        dict(children=["ORPHA:529808", "ORPHA:567544", "ORPHA:90060", "ORPHA:542643",
                       "ORPHA:529799", "ORPHA:567550", "ORPHA:567552", "ORPHA:567548",
                       "ORPHA:567546", "ORPHA:521219", "ORPHA:71519", "ORPHA:69061", "ORPHA:90062", "ORPHA:854",
                       "ORPHA:75567", "ORPHA:450322", "ORPHA:420402", "ORPHA:443084", "ORPHA:439167", "ORPHA:447881",
                       "ORPHA:439175", "ORPHA:447788", "ORPHA:3347", "ORPHA:279947", "ORPHA:294422", "ORPHA:314459",
                       "ORPHA:284227", "ORPHA:284388", "ORPHA:2820", "ORPHA:314451", "ORPHA:279882", "ORPHA:314466",
                       "ORPHA:210272", "ORPHA:1799", "ORPHA:199244", "ORPHA:178320", "ORPHA:158061", "ORPHA:157823",
                       "ORPHA:1934", "ORPHA:1935", "ORPHA:3451", "ORPHA:319205", "ORPHA:100067", "ORPHA:95409",
                       "ORPHA:100093", "ORPHA:104078", "ORPHA:99811", "ORPHA:104077", "ORPHA:2978", "ORPHA:377792"])])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.ordo_expand_multiple(["ORPHA:377792"], 3)

        expected_query = """
        MATCH (n:ORPHAterm)<-[:IS_A*0..3]-(m:ORPHAterm)
        WHERE n.orphaid IN $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """
        expected_parameters = {'orphaid': ["ORPHA:377792"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{"children": ["ORPHA:529808", "ORPHA:567544", "ORPHA:90060", "ORPHA:542643",
                                        "ORPHA:529799", "ORPHA:567550", "ORPHA:567552", "ORPHA:567548",
                                        "ORPHA:567546", "ORPHA:521219", "ORPHA:71519", "ORPHA:69061", "ORPHA:90062",
                                        "ORPHA:854",
                                        "ORPHA:75567", "ORPHA:450322", "ORPHA:420402", "ORPHA:443084", "ORPHA:439167",
                                        "ORPHA:447881",
                                        "ORPHA:439175", "ORPHA:447788", "ORPHA:3347", "ORPHA:279947", "ORPHA:294422",
                                        "ORPHA:314459",
                                        "ORPHA:284227", "ORPHA:284388", "ORPHA:2820", "ORPHA:314451", "ORPHA:279882",
                                        "ORPHA:314466",
                                        "ORPHA:210272", "ORPHA:1799", "ORPHA:199244", "ORPHA:178320", "ORPHA:158061",
                                        "ORPHA:157823",
                                        "ORPHA:1934", "ORPHA:1935", "ORPHA:3451", "ORPHA:319205", "ORPHA:100067",
                                        "ORPHA:95409",
                                        "ORPHA:100093", "ORPHA:104078", "ORPHA:99811", "ORPHA:104077", "ORPHA:2978",
                                        "ORPHA:377792"]}]


@pytest.mark.asyncio
async def test_ordo_expand_multiple_depth_zero():
    mock_execute_query = AsyncMock(return_value=[
        dict(children=["ORPHA:377792"])])

    similarity_neo4j = SimilarityNeo4j()

    with patch.object(similarity_neo4j, 'execute_query', mock_execute_query):
        result = await similarity_neo4j.ordo_expand_multiple(["ORPHA:377792"], 0)

        expected_query = """
        MATCH (n:ORPHAterm)<-[:IS_A*0..]-(m:ORPHAterm)
        WHERE n.orphaid IN $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """
        expected_parameters = {'orphaid': ["ORPHA:377792"]}
        mock_execute_query.assert_called_once_with(expected_query, expected_parameters)

        assert result == [{"children": ["ORPHA:377792"]}]





