import time

from flask import Flask, request, render_template, redirect, Blueprint, make_response
from src.helpers.amazon import authenticate_user, register_user, confirm_user, client
from flask import Flask, request, render_template, redirect, Blueprint
from src.helpers.amazon import authenticate_user
from src.model.tweet import Tweet

from src.model.user import User

bp = Blueprint('tweets', __name__)


@bp.get("/homepage")
def send_to_homepage():
    return render_template("index.html")


@bp.get("/tweets/<page>")
def get_tweets(page):
    if not page == 1:
        time.sleep(1)

    page = int(page)
    tweets = Tweet.select().order_by(Tweet.post_date.desc()).paginate(page, 2)

    if len(tweets) == 0:
        return "<div>No More</div>"

    return render_template("tweet.html", tweets=tweets, nextPage=page + 1)


@bp.post("/create")
def create_message():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    user = User.find(user_id=userID)
    tweet = Tweet(message=request.form['tweet'], user=user)
    tweet.save()
    return redirect('/users/getUser')
