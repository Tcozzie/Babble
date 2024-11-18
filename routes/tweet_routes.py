import time

import redis
from flask import request, render_template, redirect, Blueprint
from src.model.tweet import Tweet

from src.model.user import User

bp = Blueprint('tweets', __name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


@bp.get("/homepage")
def send_to_homepage():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    return render_template("index.html")


@bp.get("/tweets/<page>")
def get_tweets(page):
    userID = request.cookies.get('userId')
    if not userID:
        return "<script>window.location = '/'</script>"

    if not page == 1:
        time.sleep(1)

    page = int(page)
    tweets = Tweet.select().order_by(Tweet.post_date.desc()).paginate(page, 4)

    if len(tweets) == 0:
        return "<div style='text-align: center;'>You've scrolled to the end!</div>"

    tweet_data = []
    for tweet in tweets:
        likes = redis_client.hget(f"tweet:{tweet.id}", "likes") or 0

        has_user_liked = redis_client.sismember(f"tweet:{tweet.id}:userLikes", userID)
        heart_icon = "❤️" if has_user_liked else "🤍"

        tweet_data.append({
            "tweet": tweet,
            "likes": int(likes),
            "heart_icon": heart_icon,
        })

    return render_template("tweet.html", tweets=tweet_data, nextPage=page + 1)


@bp.post("/tweets/<int:tweet_id>/like")
def like_tweet(tweet_id):
    userID = request.cookies.get('userId')
    if not userID:
        return "<script>window.location = '/'</script>"

    has_user_liked_tweet = redis_client.sismember(f"tweet:{tweet_id}:userLikes", userID)

    if has_user_liked_tweet:
        redis_client.srem(f"tweet:{tweet_id}:userLikes", userID)
        new_likes = redis_client.hincrby(f"tweet:{tweet_id}", "likes", -1)
        liked = False
    else:
        redis_client.sadd(f"tweet:{tweet_id}:userLikes", userID)
        new_likes = redis_client.hincrby(f"tweet:{tweet_id}", "likes", 1)
        liked = True

    heart_icon = "❤️" if liked else "🤍"
    return f"<div id='like-count-{tweet_id}' style='display: flex; align-items: center; gap: 5px;'><button hx-post='/tweets/{tweet_id}/like' hx-target='#like-count-{tweet_id}' hx-swap='outerHTML' style='all:unset'>{heart_icon}</button><span style='color: #989da1; font-size: 16px; text-decoration: underline; text-decoration-color: #989da1;'>{new_likes}</span></div>"


@bp.post("/create")
def create_message():
    userID = request.cookies.get('userId')
    if not userID:
        return redirect('/')

    user = User.find(user_id=userID)
    tweet = Tweet(message=request.form['tweet'], user=user)
    tweet.save()
    return redirect('/users/getUser')
