from flask import Flask, redirect
from src.model.base import db
from src.model.user import User
from src.model.tweet import Tweet
from src.model.Comment import Comment
from routes.user_routes import bp as users_bp
from routes.tweet_routes import bp as tweets_bp

app = Flask(__name__, static_url_path='', static_folder='static')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(tweets_bp, url_prefix='/')
app.debug = True

with db:
    db.create_tables([User, Tweet, Comment], safe=True)


@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.route('/')
def index():
    return redirect("/users/signIn")


if __name__ == '__main__':
    app.run(port=8000)
