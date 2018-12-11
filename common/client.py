import asyncio

from common import utils


class Client:
    def __init__(self, loop=None):
        self.session = asyncio.get_event_loop().run_until_complete(
            utils.create_session(loop)
        )

    async def _request(self, method, url,
                       params=None, data=None, headers=None):
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        response = await self.session.request(
            method=method,
            url=self.baseurl + url,
            params=params,
            json=data,
            headers=headers,
        )
        return await response.json()
