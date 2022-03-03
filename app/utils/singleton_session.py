from aiohttp import ClientSession
from fastapi import FastAPI


class ClientContext:
    def __init__(self):
        self.session = None

    def init_aiohttp(self, app: FastAPI):
        @app.on_event("startup")
        async def startup():
            self.session = ClientSession()

        @app.on_event("shutdown")
        async def shutdown():
            if self.session:
                await self.session.close()


aiohttp_context = ClientContext()
