from numpy import single
from app.odmantic.connect import singleton_mongodb

engine = singleton_mongodb.engine
