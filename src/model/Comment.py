import datetime
from peewee import *

from src.model.base import BaseModel
from src.model.tweet import Tweet
from src.model.user import User


class Comment(BaseModel):
    message = FixedCharField(max_length=150)
    user = ForeignKeyField(User, backref='comment_user')
    corresponding_tweet = ForeignKeyField(Tweet, backref='corresponding_tweet')
    post_date = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def get_all_comments(cls, tweet):
        select = Comment.select().where(Comment.corresponding_tweet == tweet).order_by(Comment.post_date.desc())

        comments = []
        for comment in select:
            comments.append(comment)

        return comments
