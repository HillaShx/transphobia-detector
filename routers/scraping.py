from datetime import datetime

import tweepy
from facebook_scraper import get_posts

from DTO.post import FacebookPost, TwitterPost
from config import bearer_token
from services.csv_helper import CSVWriter
from services.mail_helper import send_yagmail


def fetch_posts_for_id(ids):
    posts = []
    for id in ids:
        id = id.strip()
        posts_itr = get_posts(id, pages=10, options={"posts_per_page": 10})
        for post in posts_itr:
            posts.append(
                FacebookPost(
                    pid=post.get("post_id"),
                    username=post.get("username"),
                    post_text=post.get("post_text"),
                    shared_text=post.get("shared_text"),
                    timestamp=datetime.fromtimestamp(post.get("timestamp"))
                )
            )
    return posts


def read_ids_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines


def scrape_facebook():
    ids = read_ids_from_file("facebook_ids_for_scraping.txt")
    posts = fetch_posts_for_id(ids)
    csv_writer = CSVWriter(FacebookPost)
    output_path = f"storage/facebook/{datetime.date(datetime.now())}.csv"
    csv_writer.write(posts, output_path)
    send_yagmail("hilla.sh@gmail.com", output_path)
    return posts


def scrape_twitter():
    """
    Faulty; Gives out messy data
    :return:
    """
    ids = read_ids_from_file("twitter_ids_for_scraping.txt")
    client = tweepy.Client(bearer_token=bearer_token)
    posts = []
    for id in ids:
        id = id.strip()
        new_tweets = client.get_users_tweets(id, tweet_fields=['id', 'text', 'possibly_sensitive', 'lang', 'created_at'])
        with open("tweets.txt", "w") as f:
            for tweet in new_tweets.data:
                f.write(str(tweet))
        user = client.get_user(id=id)
        for tweet in new_tweets.data:
            posts.append(
                TwitterPost(
                    pid=tweet.id,
                    username=user.data.username,
                    text=tweet.text,
                    created_at=tweet.created_at,
                    lang="he" if tweet.lang == "iw" else tweet.lang,
                    possibly_sensitive=tweet.possibly_sensitive
                )
            )
    csv_writer = CSVWriter(TwitterPost)
    output_path = f"storage/twitter/{datetime.date(datetime.now())}.csv"
    csv_writer.write(posts, output_path)
    send_yagmail("hilla.sh@gmail.com", output_path)
    return posts
