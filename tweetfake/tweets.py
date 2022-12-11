import base64
import hashlib
import os
import re
from typing import Tuple, List

import requests
from requests_oauthlib import OAuth2Session

from tweetfake.model.filter_posts import get_prompt
from tweetfake.model.generate import GeneratedText, generate_text
from tweetfake.model.preprocessing import Corpus, Post

scopes = ["tweet.read", "users.read"]

def generate_challenge() -> Tuple[str, str]:
    # generate verifier and challenge
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    return code_verifier, code_challenge


def make_token(client_id: str, redirect_uri: str) -> OAuth2Session:
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

def get_tweets(token: dict, username: str):
    userid_response = requests.get(
        f"https://api.twitter.com/2/users/by/username/{username}",
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        },
    )
    userid = userid_response.json()["data"]["id"]
    print(username, userid)

    posts_response = requests.get(
        f"https://api.twitter.com/2/users/{userid}/tweets?exclude=retweets&tweet.fields=public_metrics,created_at",
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        }
    )
    return posts_response.json()


def make_corpus(response: dict) -> Corpus:
    posts = []
    for p in response["data"]:
        post = Post(
            p["created_at"],
            type="Twitter",
            caption=p["text"],
            likes=p["public_metrics"]["like_count"],
        )
        posts.append(post)

    return Corpus(*posts)


def generate_tweets(token: dict, username: str, temperature: float) -> List[GeneratedText]:
    response = get_tweets(token, username)
    corpus = make_corpus(response)
    prompt = get_prompt(corpus)
    return generate_text(prompt, temperature)


