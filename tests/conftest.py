import asyncio
import nest_asyncio
from pytest import fixture
from fastapi.testclient import TestClient
from app.models.plot import Plot, Queue
from app import app_api
from app.models import run


@fixture(scope='session')
async def create_db():
    await run(generate_schemas=True)

@fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@fixture(autouse=True, scope='function')
async def drop_test_database():
    await asyncio.gather(
        Queue.all().delete(),
        Plot.all().delete(),

    )
    yield


@fixture()
def client():
    nest_asyncio.apply()
    with TestClient(app=app_api) as test_client:
        yield test_client


@fixture
def queue_create(client):
    client.get('/plot/queue/create')
    client.get('/plot/queue/create')
    response = client.get('/plot/queue/create')
    assert response.json()['waiting'] == 3
    return response.json()
