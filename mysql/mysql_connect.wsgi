#!/usr/bin/env python
import logging
import sys

#sys.path.insert(0,'/var/www/cgi-bin/venv')
sys.path.insert(0,'/var/www/cgi-bin')

from main import app as application
application.secret_key = '1234abcd'


if __name__ == '__main__':
    print("hello from exam_app.wsgi")