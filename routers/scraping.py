from fastapi import APIRouter
from facebook_scraper import get_posts
from datetime import datetime

from DTO.post import FacebookPost

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def fetch_posts_for_id(id):
    posts_itr = get_posts(id, pages=10, options={"posts_per_page": 10})
    posts = []
    for post in posts_itr:
        posts.append(
            FacebookPost(
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
        return lines[0]


@router.get("/facebook")
async def scrape_facebook():
    ids = read_ids_from_file("facebook_ids_for_scraping.txt")
    posts = fetch_posts_for_id(ids)
    return posts
