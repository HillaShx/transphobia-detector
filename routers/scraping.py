from fastapi import APIRouter
from facebook_scraper import get_posts
import tweepy
import config
import pandas as pd

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def fetch_posts_for_id(id):
    posts_itr = get_posts(id, pages=10, options={"posts_per_page": 10})
    return [post for post in posts_itr]

def read_ids_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [l.rstrip('\n') for l in lines]

@router.get("/facebook")
async def scrape_facebook():
    ids = read_ids_from_file("facebook_ids_for_scraping.txt")
    posts = fetch_posts_for_id(ids)
    print(posts)
    return

@router.get("/twitter")
async def scrape_twitter():
    ids = read_ids_from_file("twitter_ids_for_scraping.txt")
    df = pd.DataFrame(columns=["id", "username", "text", "created_at", "lang", "possibly_sensitive"])
    client = tweepy.Client(bearer_token=config.bearer_token)
    for id in ids:
        new_tweets = client.get_users_tweets(id, tweet_fields=['id', 'text', 'possibly_sensitive', 'lang', 'created_at'])
        user = client.get_user(id=id)
        for tweet in new_tweets.data:
            l = {
                "id": tweet.id,
                "username": user.data.username,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "lang": "he" if tweet.lang == "iw" else tweet.lang,
                "possibly_sensitive": tweet.possibly_sensitive,
            }
            df = pd.concat([df, pd.DataFrame([l])], ignore_index=True)
    return
