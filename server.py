#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import os.path
import sys

BASEURL = '/stab'

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):            
        possible_name = self.path.strip("/")+'.html'
        if os.path.isfile(possible_name):
            # extensionless page serving
            self.path = possible_name

        if self.path.startswith(BASEURL):
            self.path = self.path[len(BASEURL):]

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler

port = 8000
if len(sys.argv) > 1:
    try:
        p = int(sys.argv[1])
        port = p
    except ValueError:
        print "port value provided must be an integer"

print "serving on port {0}".format(port)
server = SocketServer.TCPServer(('0.0.0.0', port), Handler)
try:
    server.serve_forever()
except:
    server.shutdown()
    server.server_close()
