import base64
import hashlib
import os
import re

import requests
from flask import Flask, request, session, redirect
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(50)


client_id = os.environ.get("TWITTER_API_KEY")
client_secret = os.environ.get("TWITTER_API_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
deploy_url = "https://3ce2-84-115-219-119.eu.ngrok.io"
redirect_uri = deploy_url + "/oauth/callback"

scopes = ["tweet.read", "users.read"]

# generate verifier and challenge
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")


def make_token():
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
        f"https://api.twitter.com/2/users/{userid}/tweets?exclude=retweets&tweet.fields=public_metrics",
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        }
    )
    print(posts_response.json())


@app.route("/")
def demo():
    global twitter
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    print(authorization_url)
    print(state)
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    print("Callback")
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    st_token = '"{}"'.format(token)
    print(st_token)
    get_tweets(token, "billgates")



if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
