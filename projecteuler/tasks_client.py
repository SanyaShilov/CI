from common import client
from common import constants


class TasksClient(client.Client):
    def __init__(self, loop=None):
        super().__init__(loop=loop)
        self.baseurl = 'http://localhost:{}'.format(constants.TASKS_PORT)

    async def search_tasks(self, **data):
        return await self._request(
            method='POST',
            url='/tasks/search',
            data=data,
        )

    async def search_proposed_tasks(self, **data):
        return await self._request(
            method='POST',
            url='/proposed_tasks/search',
            data=data,
        )

    async def count(self):
        return await self._request(
            method='GET',
            url='/tasks/count',
        )

    async def proposed_count(self):
        return await self._request(
            method='GET',
            url='/proposed_tasks/count',
        )

    async def get_task(self, task_id):
        return await self._request(
            method='GET',
            url='/tasks',
            params={'id': task_id},
        )

    async def get_proposed_task(self, task_id):
        return await self._request(
            method='GET',
            url='/proposed_tasks',
            params={'id': task_id},
        )

    async def solve(self, task_id):
        return await self._request(
            method='POST',
            url='/tasks/solve',
            params={'id': task_id},
        )

    async def propose(self, **data):
        return await self._request(
            method='POST',
            url='/proposed_tasks',
            data=data
        )

    async def publish(self, **data):
        return await self._request(
            method='POST',
            url='/tasks',
            data=data
        )

    async def update_proposed_task(self, task_id, **data):
        return await self._request(
            method='PATCH',
            url='/proposed_tasks',
            data=data,
            params={
                'id': task_id
            }
        )

    async def delete_proposed_task(self, task_id):
        return await self._request(
            method='DELETE',
            url='/proposed_tasks',
            params={
                'id': task_id
            }
        )
