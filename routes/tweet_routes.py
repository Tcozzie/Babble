from flask import Flask, request, render_template, redirect, Blueprint, make_response
from src.helpers.amazon import authenticate_user, register_user, confirm_user, client
from flask import Flask, request, render_template, redirect, Blueprint
from src.helpers.amazon import authenticate_user
from src.model.tweet import Tweet

from src.model.user import User

bp = Blueprint('tweets', __name__)


@bp.get("/homepage")
def send_to_homepage():
    tweets = Tweet.all_tweets()

    return render_template("index.html", tweets=tweets)

@bp.post("/create")
def create_message():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    user = User.find(user_id=userID)
    tweet = Tweet(message=request.form['tweet'], user=user)
    tweet.save()
    return redirect('/users/getUser')
