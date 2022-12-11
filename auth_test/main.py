import os

from flask import Flask, request, session, redirect, render_template, url_for
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

from auth_test.tweets import make_token, generate_challenge, get_tweets, generate_tweets

app = Flask(__name__)
app.secret_key = os.urandom(50)


client_id = os.environ.get("TWITTER_API_KEY")
client_secret = os.environ.get("TWITTER_API_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
deploy_url = "https://3ce2-84-115-219-119.eu.ngrok.io"
redirect_uri = deploy_url + "/oauth/callback"

code_verifier, code_challenge = generate_challenge()
twitter_session = make_token(client_id, redirect_uri)


@app.route("/twitter/")
def demo():
    global twitter_session
    authorization_url, state = twitter_session.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route('/')
def index():
    return render_template(
        'index.html',
        tweets=[t[0] for t in session["generated"]] if "generated" in session else [],
        logged_in="oauth_token" in session,
        background_image=os.path.join('static', 'fake_image.png'),
    )


@app.route('/tweets/', methods=['POST'])
def submit_credentials():
    username = request.form['tw_username']

    texts = generate_tweets(session["oauth_token"], username, temperature=3.0)
    session["generated"] = texts
    return redirect(url_for(".index"))


@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token = twitter_session.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    session["oauth_token"] = token
    return redirect(url_for(".index"))



if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
