
from flask import Blueprint, render_template, request
from tweetfake.website.templates import *
from tweetfake.model.preprocessing import *


views = Blueprint('views', __name__)


@views.route('/landing')
def landing():

    return render_template("landing.html",
        depth2Var=False,
        summary_text=''
    )



@views.route('/landing', methods=('GET', 'POST'))
def submit_credentials():
    if request.method == 'POST':

        ig_handle = request.form.get('ig_handle')
        tw_handle = request.form.get('tw_handle'), 
        fb_handle = request.form.get('fb_handle'), 

        ipp = InstagramPreProcessor(ig_handle)
        posts = ipp.getPosts()

        for post in posts: 
            
            print('\n\n\n')
            for key, value in post.__dict__.items():
                print(key, value) 

        corpus = Corpus(*posts)

        # ---- call server to run model --- get summary

        summary_text = 'In 2022, I graduated from CSUN with BSc in EE, \
            went to the Bahamas in the Summer, and finished the year off \
            getting engaged in Dubai!!'

    return render_template("landing.html",
        depth2Var=True,
        summary_text=summary_text
    )


