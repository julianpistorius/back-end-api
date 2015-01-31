__author__ = 'Marnee Dearman'
from wsgiref.simple_server import make_server

from app import api

httpd = make_server('', 8000, api)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()

# Alternative: serve one request, then exit
httpd.handle_request()