# !/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'NereWARin'

from flask import Flask, url_for, request, render_template
from flask_probe01 import app
from functools import wraps
import redis
import random
from warnings import warn

# def my_decorator(f):
#     @wraps(f)
#     def wrapper(*args, **kwds):
#         return f(*args, **kwds)
#     return wrapper

# connect to redis data store
# DEFAULT PARAMETERS
# r = redis.StrictRedis()
# r = redis.StrictRedis(host="localhost", port=6379, db=0)
# add parameters to cast responses to unicode
r = redis.StrictRedis(host="localhost", port=6379, db=0, charset="UTF-8", decode_responses=True)
# check redis service is available

try:
    response = r.client_list()
except redis.ConnectionError:
    #your error handlig code here
    warn("You need to start redis servise from task manager (Windows)")
else:
    print "redis is active"
    # print "redis response = %s" % response

# we will name initially route url as server
# with a app.route we can expand urls
# print "\nkeys"
# print [key for key in r.keys()]
print "\nwhat in DB now?"
keys = r.keys()
for key in keys:
    # print ".", key
    # print "_", r.get(key), "\n"
    # print "key.split(\":\")", key.split(":")[0]
    # delete empty questions
    if len(key.split(":")[0])  < 1 :
        # print "AHAAA", key
        r.delete(key)
        # r.
for key in keys:
    print ".", key
    print "_", r.get(key), "\n"

# # keys = [key.encode("UTF-8") for key in r.keys()]
# vals = r.mget(keys)
# print "\nvalues"
#
# for val in vals:
#     # for v in val:
#     #     print v
#     print vals
# # kv = zip(keys, vals)
# # print kv


# server/
@app.route('/')
def hello():
    # href is a link tag
    # url_for('create') = calling create func
    createLink = "<a href='" + url_for('create') + "'>Create a question</a>"
    print " url_for('create')",  url_for('create')
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
@app.route('/create', methods=["GET", "POST"])
def create():
     # return "<h2>This is the create page!</h2>"
    if request.method == "GET":
        # send the user the form
        return render_template('CreateQuestion.html')

    elif request.method == "POST":
        print "create - post"
        # read form data and save it
        title = request.form["title"]
        question = request.form["question"]
        answer = request.form["answer"]

        # store data in database
        # key name will be whatever title they typed in : question
        # e.g. Music:question
        # e.g. Music:answer
        try:
            r.set(title+':question', question) # ":" is not required
            r.set(title+':answer', answer)
        # except:
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
            x, y = inst.args
            print 'x =', x
            print 'y =', y
        else:
            print "ok redis.set %s:question = %s, %s:answer = %s" % (title, question, title, answer)

        # let user redirect to random question after he add his question
        rnd_question = random.choice(r.keys()).split(":")[0]
        return render_template('CreatedQuestion.html', question = question, rnd_question = rnd_question)

    # elif request:
    else:

        return "<h2>Invalid request! unknown method %s for route('/create')</h2>" % request.method



# server/question/<title>
# view on screen just last url piece (title)
@app.route('/question/<title>', methods=["GET", "POST"])
def question(title):
    # return '<h2>' + title + '</h2>'
    if request.method == "GET":
        # send the user the form
        question =  r.get(title+':question')

        # read question from data store
        return render_template('AnswerQuestion.html', question = question)

    elif request.method == "POST":
        # user has attemped answer. Check if its correct
        submittedAnswer = request.form["submittedAnswer"]

        # read answer from data store
        answer = r.get(title+':answer')
        try:
            answer.lower()
        except:
            raise Exception, "answer %s has type %s and has no method .lower()" % (answer, type(answer))
        try:
            submittedAnswer.lower()
        except:
            raise Exception, "answer %s has type %s and has no method .lower()" % (submittedAnswer, type(submittedAnswer))

        print "submittedAnswer = %s, answer = %s" % (submittedAnswer, answer)
        if answer.lower() == submittedAnswer.lower():
            return "Correct!"
            # return render_template("Correct.html")
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer)

    else:
        return "<h2>Invalid request! unknown method %s for route('/question/<%s>')</h2>" % (request.method, title)


print "redis.__version__ %s" % redis.__version__
app.run()

# TODO make button in CreatedAnswer to move to Answer.html