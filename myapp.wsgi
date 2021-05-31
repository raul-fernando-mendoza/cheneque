#!/usr/bin/env python
import sys
def application(environ, start_response):
    status = '200 OK'

    msg = 'Hello World python version:' + sys.prefix + " " + sys.version
    output = str.encode(msg)

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]