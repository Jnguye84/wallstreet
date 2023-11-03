#!/usr/bin/env python
from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import request, redirect
from wtforms.validators import InputRequired

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
import mostfrequent
from urllib.request import Request, urlopen

from document_classify import *
from mostfrequent import *

# Create the application.
APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'you-will-never-guess'

class UploadStringForm(FlaskForm):
    user_string = StringField('String', validators=[InputRequired()])
    submit = SubmitField('Send Link')

@APP.route('/')
def home():
    return render_template('index.html')

@APP.route('/url', methods=['GET','POST'])
def url():
    form = UploadStringForm()
    if form.validate_on_submit():
        user_string = form.user_string.data
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True

        def text_from_html(body):
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            return u" ".join(t.strip() for t in visible_texts)
            
        # Set the User-Agent header to mimic a web browser
        req = Request(
            url=user_string, #this is where the variable needs to go
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()
        article_str = text_from_html(webpage) #string from the entire webpage
        arr_prob,classify, lst = DocClassifyExcel(article_str) #input needs to be string or list
        arr_prob = arr_prob*100
        arr_prob = "{:.6f}".format(arr_prob)
        return render_template('display_word.html', arr_prob=arr_prob, classify=classify, common_words=lst)
    return render_template('url.html', form = form)

if __name__ == '__main__':
    APP.debug=True
    APP.run()
