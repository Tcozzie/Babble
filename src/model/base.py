import logging

from peewee import Model, SqliteDatabase

db = SqliteDatabase('babble.db')

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class BaseModel(Model):
    class Meta:
        database = db


__all__ = ['BaseModel']
