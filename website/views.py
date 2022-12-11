
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
        background_image=os.path.join('static', 'fake_image.png')
    )


# @views.route('/landing', methods=('GET', 'POST'))
# def submit_credentials():
#     if request.method == 'POST':
#
#         # ig_handle = request.form.get('ig_handle')
#         # tw_handle = request.form.get('tw_handle'),
#         # fb_handle = request.form.get('fb_handle'),
#
#         # ipp = InstagramPreProcessor(ig_handle)
#         # posts = ipp.getPosts()
#         #
#         # for post in posts:
#         #
#         #     print('\n\n\n')
#         #     for key, value in post.__dict__.items():
#         #         print(key, value)
#         #
#         # corpus = Corpus(*posts)
#
#         # ---- call server to run model --- get summary
#
#         summary_text = 'In 2022, I graduated from CSUN with BSc in EE, \
#             went to the Bahamas in the Summer, and finished the year off \
#             getting engaged in Dubai!!'
#
#     return render_template("landing.html",
#         depth2Var=True,
#         summary_text=summary_text
#     )

@views.route('/tweet', methods=['POST'])
def submit_credentials():
    tw_username = request.form['tw_username']

    summary_text = 'In 2022, I graduated from CSUN with BSc in EE, \
                went to the Bahamas in the Summer, and finished the year off \
                getting engaged in Dubai!!'

    tweets.append(summary_text)
    return redirect('/')



