from odmantic import Model

from app.nosql.odmantic import mongo_db
from app.nosql.odmantic.model import Request, Response, Book


async def clear_models(model: Model):
    instance_list = await mongo_db.engine.find(model, {})
    for instance in instance_list:
        await mongo_db.engine.delete(instance)


async def clear_all():
    await clear_models(Request)
    await clear_models(Response)
    await clear_models(Book)
