from similarity_neo4j import SimilarityNeo4j
from unittest.mock import AsyncMock
import pytest

SimilarityNeo4j.init_driver()


@pytest.mark.asyncio
async def test_verify_success():

    mock_driver = AsyncMock()
    mock_driver.verify_connectivity = AsyncMock(return_value=None)
    mock_driver.verify_authentication = AsyncMock(return_value=None)

    similarity_neo4j = SimilarityNeo4j(driver=mock_driver)

    assert await similarity_neo4j.verify() is True


@pytest.mark.asyncio
async def test_verify_failed_connection():

    mock_driver = AsyncMock()
    mock_driver.verify_connectivity = AsyncMock(side_effect=Exception('Connection failed'))
    mock_driver.verify_authentication = AsyncMock(return_value=None)

    similarity_neo4j = SimilarityNeo4j(driver=mock_driver)

    assert await similarity_neo4j.verify() is False


@pytest.mark.asyncio
async def test_verify_failed_authentication():
    mock_driver = AsyncMock()
    mock_driver.verify_connectivity = AsyncMock(return_value=None)
    mock_driver.verify_authentication = AsyncMock(side_effect=Exception('Authentication failed'))

    similarity_neo4j = SimilarityNeo4j(driver=mock_driver)

    assert await similarity_neo4j.verify() is False


@pytest.mark.asyncio
async def test_close():
    mock_driver = AsyncMock()
    mock_driver.close = AsyncMock(return_value=None)

    similarity_neo4j = SimilarityNeo4j(driver=mock_driver)

    await similarity_neo4j.close()

    mock_driver.close.assert_called_once()
