# !/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'NereWARin'

from flask import Flask, url_for, request, render_template
from flask_probe01 import app
from functools import wraps

# def my_decorator(f):
#     @wraps(f)
#     def wrapper(*args, **kwds):
#         return f(*args, **kwds)
#     return wrapper



# we will name initially route url as server
# with a app.route we can expand urls

# server/
@app.route('/')
def hello():
    # href is a link tag
    # url_for('create') = calling create func
    createLink = "<a href='" + url_for('create') + "'>Create a question</a>"
    return """<html>
                <head>
                    <title> hello head! </title>
                </head>
                <body>
                    <h1> %s </h1>
                </body>
            </html>""" % (createLink)
            # </html>""" % ("привет киса!\n" + createLink)
    # return 'Hello my fist Flask website!' \
    #        'Gorbachev Arsenii 04.07.2015 nerewarin89@mail.ru'


# @app.route('/create')
@app.route('/create!', methods=["GET", "POST"])
def create():
     # return "<h2>This is the create page!</h2>"
    if request.method == "GET":
        # send the user the form
        return render_template('CreateQuestion.html')

    elif request.method == "POST":
        # read form data and save it
        title = request.form["title"]
        question = request.form["question"]
        answer = request.form["answer"]
        # store data in database
        return render_template('CreatedQuestion.html', question = question)
    else:

        return "<h2>Invalid request! unknown method %s for route('/create')</h2>" % request.method


# server/question/<title>
# view on screen just last url piece (title)
@app.route('/question/<title>', methods=["GET", "POST"])
def question(title):
    # return '<h2>' + title + '</h2>'
    if request.method == "GET":
        # send the user the form
        question = "Question here."

        # read question from data store
        return render_template('AnswerQuestion.html', question = question)

    elif request.method == "POST":
        # user has attemped answer. Check if its correct
        submittedAnswer = request.form["submittedAnswer"]

        # read answer from data store
        answer = "Answer"
        if submittedAnswer == answer:
            return render_template("Correct.html")
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer)

    else:
        return "<h2>Invalid request! unknown method %s for route('/question/<%s>')</h2>" % (request.method, title)

app.run()