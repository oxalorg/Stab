#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import os.path
import sys


BASEURL = '/'
port = 5763
if len(sys.argv) > 1:
    BASEURL = sys.argv[1]


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


print "serving on port {0}".format(port)
server = SocketServer.TCPServer(('0.0.0.0', port), Handler)
try:
    server.serve_forever()
except:
    print "Shutting down server.."
finally:
    server.shutdown()
    server.server_close()
