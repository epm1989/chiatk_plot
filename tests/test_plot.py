from pytest import mark
from app.models.plot import Queue, Plot
import asyncio

@mark.asyncio
async def test_queue_start_stop_success(create_db, client, queue_create):

    response = client.get('/plot/queue/status')

    assert response.json()['waiting'] == queue_create['waiting']

    response = client.get('/plot/start')
    pid = response.json()['pid']
    await asyncio.sleep(6)

    response = client.get('/plot/queue/status')
    assert response.json()['running'] == 1
    assert response.json()['waiting'] == 2

    response = client.get('/plot/all')
    assert len(response.json()['result']) == 1

    response = client.get(f'/plot/stop/{pid}')
    assert response.json()['result'] is True
    assert response.json()['message'] == f'stopped {pid}'




