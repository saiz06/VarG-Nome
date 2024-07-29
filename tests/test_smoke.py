import pytest
from main import app, startup, graceful_shutdown


@pytest.mark.asyncio
async def test_index_smoke():
    test_client = app.test_client()
    await startup()
    
    response = await test_client.get('/')
    assert response.status_code == 200
    data = await response.get_data(as_text=True)
    assert data == 'OK'

    await graceful_shutdown()


@pytest.mark.asyncio
async def test_get_similar_hpo_smoke():
    test_client = app.test_client()
    await startup()

    test_data = {
        "hpoTerms": ["HP:0000001", "HP:0000002"],
        "threshold": 0.75
    }
    response = await test_client.post('/similarity/hpo', json=test_data)
    assert response.status_code == 200
    assert response.content_type == "application/json"

    await graceful_shutdown()


@pytest.mark.asyncio
async def test_get_similar_ordo_smoke():
    test_client = app.test_client()
    await startup()

    test_data = {
        "ordoTerms": ["ORPHA:377794", "ORPHA:377795"],
        "matchScale": 1,
        "threshold": 0.9,
    }

    response = await test_client.post('/similarity/ordo', json=test_data)
    assert response.status_code == 200
    assert response.content_type == "application/json"

    await graceful_shutdown()


@pytest.mark.asyncio
async def test_expand_hpo_smoke():
    test_client = app.test_client()
    await startup()

    test_data = {
        "hpoTerms": ["HP:0000001", "HP:0000002"]
    }

    response = await test_client.post('/expand/hpo', json=test_data)
    assert response.status_code == 200
    assert response.content_type == "application/json"

    await graceful_shutdown()
