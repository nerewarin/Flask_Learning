# !/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'NereWARin'

from flask import Flask

# import jinja2
app = Flask(__name__)

# wsgi_app = app.wsgi_app
from routes import *





# launching our server
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
