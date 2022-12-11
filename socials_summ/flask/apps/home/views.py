# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/landing')
def landing():
    return render_template('home/landing.html',
                           depth2Var=False,
                           summary_text='')


@blueprint.route('/landing', methods=('GET', 'POST'))
def submit_credentials():
    if request.method == 'POST':

        ig_handle = request.form.get('ig_handle')
        tw_handle = request.form.get('tw_handle'),
        fb_handle = request.form.get('fb_handle'),

        # ipp = InstagramPreProcessor(ig_handle)
        # posts = ipp.getPosts()
        #
        # for post in posts:
        #
        #     print('\n\n\n')
        #     for key, value in post.__dict__.items():
        #         print(key, value)
        #
        # corpus = Corpus(*posts)

        # ---- call server to run model --- get summary

        summary_text = 'In 2022, I graduated from CSUN with BSc in EE, \
            went to the Bahamas in the Summer, and finished the year off \
            getting engaged in Dubai!!'

    return render_template("home/landing.html",
                           depth2Var=True,
                           summary_text=summary_text
                           )














# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#
#     try:
#
#         if not template.endswith('.html'):
#             template += '.html'
#
#         # Detect the current page
#         # segment = get_segment(request)
#
#         # Serve the file (if exists) from app/templates/home/FILE.html
#         # return render_template("home/" + template, segment=segment)
#         return render_template("home/" + template)
#
#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404
#
#     except:
#         return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
# def get_segment(request):
#
#     try:
#
#         segment = request.path.split('/')[-1]
#
#         if segment == '':
#             segment = 'index'
#
#         return segment
#
#     except:
#         return None
