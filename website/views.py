
from flask import Blueprint, render_template, request, redirect, url_for
from website.templates import *
from model.preprocessing import *
import os

tweets = []

views = Blueprint('views', __name__)

# redirecting to landing page on start
@views.route('/')
def route_default():
    return redirect(url_for('views.landing'))


@views.route('/landing')
def landing():
    return render_template("landing.html",
        depth2Var=False,
        # summary_text=''
        tweets = tweets,
        logo_image=os.path.join('static', 'logo_image.jpg'),
    )


@views.route('/tweet', methods=['POST'])
def submit_credentials():
    tw_username = request.form['tw_username']

    summary_text = 'In 2022, I graduated from CSUN with BSc in EE, \
                went to the Bahamas in the Summer, and finished the year off \
                getting engaged in Dubai!!'

    tweets.append(summary_text)
    return redirect('/')



