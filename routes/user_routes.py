import redis
from flask import make_response, request, render_template, redirect, Blueprint
from src.helpers.amazon import register_user, authenticate_user
from src.model.tweet import Tweet

from src.model.user import User

bp = Blueprint('users', __name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


@bp.get("/getUser")
def get_user():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    user = User.find(user_id=userID)
    all_my_tweets = Tweet.all_logged_in_user_tweets(logged_in_user=user)

    tweet_data = []
    for tweet in all_my_tweets:
        likes = redis_client.hget(f"tweet:{tweet.id}", "likes") or 0

        has_user_liked = redis_client.sismember(f"tweet:{tweet.id}:userLikes", userID)
        heart_icon = "❤️" if has_user_liked else "🤍"

        tweet_data.append({
            "tweet": tweet,
            "likes": int(likes),
            "heart_icon": heart_icon,
        })

    return render_template("create_message.html", user=user, tweets=tweet_data)


@bp.get("/signIn")
def sign_In():
    userID = request.cookies.get('userId')

    # If there is already a valid cookie. Just send them to the homepage
    if userID:
        return redirect('/homepage')

    return render_template("signIn.html")


@bp.post('/signIn')
def sign_in():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    auth = authenticate_user(username, password)
    if not auth:
        return render_template("signIn.html", errorMessage="Username or Password is incorrect")

    # If user is in AWS and not in the DB. Add the user to the DB
    if User.find(user_id=auth['userId']) is None:
        User.insert(username=username, email=auth['email'], userID=auth['userId'],
                    profilePic="/img/noProfile.jpeg").execute()
    # Create a response object for redirect
    response = make_response(redirect('/homepage'))

    # Getting userId from auth
    user_id = auth['userId']

    # Store the userId in a cookie
    response.set_cookie("userId", user_id, max_age=3600, httponly=True, secure=False)

    return response


@bp.get('/logout')
def logout():
    response = make_response(redirect('/'))

    # Deleting user cookie so they have to sign in again
    response.delete_cookie("userId")

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
        return render_template("signUp.html", errorMessage="There was en error signing up. Please refresh the page "
                                                           "and try again")

    User.insert(username=username, email=email, userID=auth['UserSub'],
                profilePic="/img/noProfile.jpeg").execute()

    # Signing in the user
    auth = authenticate_user(username, password)

    if not auth:
        return render_template("signIn.html", errorMessage="There was an issue signing you in after sign up. please "
                                                           "try signing in")

    # Create a response object for redirect
    response = make_response(redirect('/homepage'))

    # Getting userId from auth
    user_id = auth['userId']

    # Store the userId in a cookie
    response.set_cookie("userId", user_id, max_age=3600, httponly=True, secure=False)

    return response
