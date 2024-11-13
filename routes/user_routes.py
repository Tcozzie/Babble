from flask import Flask, request, render_template, redirect, Blueprint, make_response
from src.helpers.amazon import authenticate_user, register_user, confirm_user, client
from flask import Flask, request, render_template, redirect, Blueprint
from src.helpers.amazon import authenticate_user
from src.model.tweet import Tweet

from src.model.user import User

bp = Blueprint('users', __name__)


@bp.get("/getUser")
def get_user():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    user = User.find(user_id=userID)
    all_my_tweets = Tweet.all_logged_in_user_tweets(logged_in_user=user)

    return render_template("create_message.html", user=user, tweets=all_my_tweets)


@bp.get("/signIn")
def sign_In():
    return render_template("signIn.html")


@bp.post('/signIn')
def sign_in():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    auth = authenticate_user(username, password)
    if not auth:
        return "<div>There was an error signing in. Please refresh the page and try again.</div>"

    # If user is in AWS and not in the DB. Add the user to the DB
    if User.find(user_id=auth['userId']) is None:
        User.insert(username=username, email=auth['email'], userID=auth['userId'],
                    profilePic="https://randomuser.me/api/portraits/thumb/men/75.jpg").execute()
    # Create a response object for redirect
    response = make_response(redirect('/homepage'))

    # Getting userId from auth
    user_id = auth['userId']

    # Store the userId in a cookie
    response.set_cookie("userId", user_id, max_age=3600, httponly=True, secure=False)

    return response


@bp.get("/signUp")
def signUp():
    return render_template("signUp.html")


@bp.post("/signUp")
def sign_up():
    data = request.form
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    auth = register_user(username, password, email)

    # checking if the sign-up was successful
    if isinstance(auth, Exception):
        return "<div>There was en error signing up. Please refresh the page and try again.</div>"

    User.insert(username=username, email=email, userID=auth['UserSub'],
                profilePic="https://randomuser.me/api/portraits/thumb/men/75.jpg").execute()

    # Signing in the user
    auth = authenticate_user(username, password)

    # Create a response object for redirect
    response = make_response(redirect('/homepage'))

    # Getting userId from auth
    user_id = auth['userId']

    # Store the userId in a cookie
    response.set_cookie("userId", user_id, max_age=3600, httponly=True, secure=False)

    return response
