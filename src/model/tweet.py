import datetime
from zoneinfo import ZoneInfo
from peewee import *

from src.model.base import BaseModel
from src.model.user import User


class Tweet(BaseModel):
    message = CharField()
    user = ForeignKeyField(User, backref='tweets')
    post_date = DateTimeField(default=lambda: datetime.datetime.now(ZoneInfo("America/Denver")).strftime('%b %d, %Y - %I:%M %p'))

    @classmethod
    def all_tweets(cls):
        select = Tweet.select().order_by(Tweet.post_date.desc())
        return select

    @classmethod
    def all_logged_in_user_tweets(cls, logged_in_user):
        select = Tweet.select().where(Tweet.user == logged_in_user).order_by(Tweet.post_date.desc())
        return select

    @classmethod
    def find(cls, input_id):
        select = Tweet.get_or_none(Tweet.id == int(input_id))
        return select


