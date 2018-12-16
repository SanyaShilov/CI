import asyncio
import collections


async def test_register(db, users_client):
    requests = []
    for _ in range(10):
        requests.append(
            users_client.post(
                '/register',
                json={
                    'login': 'login',
                    'password': 'password',
                }
            )
        )
    responses = await asyncio.gather(*requests)
    statuses = collections.defaultdict(int)
    for response in responses:
        statuses[response.status] += 1
    assert statuses == {
        201: 1,
        422: 9
    }
    count = await db.users.count_documents({
        'login': 'login',
        'password': 'password'
    })
    assert count == 1


async def test_sign_in(db, users_client):
    requests = []
    for _ in range(10):
        requests.append(
            users_client.post(
                '/sign_in',
                json={
                    'login': 'login0',
                    'password': 'password0',
                }
            )
        )
    responses = await asyncio.gather(*requests)
    statuses = collections.defaultdict(int)
    user = await db.users.find_one({
        'login': 'login0',
        'password': 'password0'
    })
    for response in responses:
        statuses[response.status] += 1
        body = await response.json()
        assert body['token'] == user['token']
    assert statuses == {
        200: 10
    }


async def test_solve(db, users_client):
    requests = []
    for _ in range(10):
        requests.append(
            users_client.post(
                '/solve',
                json={
                    'task_id': 2
                },
                headers={
                    'projecteuler-user-token': '5be12c3c4b3e4d019fa99fa3'
                }
            )
        )
    responses = await asyncio.gather(*requests)
    statuses = collections.defaultdict(int)
    for response in responses:
        statuses[response.status] += 1
    assert statuses == {
        200: 1,
        422: 9
    }
    user = await db.users.find_one({
        'token': '5be12c3c4b3e4d019fa99fa3'
    })
    assert user['solutions_count'] == 2
