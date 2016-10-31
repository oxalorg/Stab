#!/usr/bin/env python3
import http.server
import socketserver
import os.path
import sys

BASEURL = '/'
port = 5763
if len(sys.argv) > 1:
    BASEURL = sys.argv[1]


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):            
        print('Requested path:' + self.path)
        if self.path.startswith('/') and not self.path.startswith(BASEURL):
            print('1st rule ' + self.path)
            self.send_error(404, 'Not found. Make sure you entered ' +BASEURL+ ' in the url')
            self.path = None
        elif self.path.startswith(BASEURL):
            self.path = self.path[len(BASEURL):]
        if self.path:
            possible_name = self.path.strip("/")+'.html'
            if os.path.isfile(possible_name):
                # extensionless page serving
                self.path = possible_name
            print('Altered path relative to `site_baseurl`:' + str(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler


print ('serving on port {0}'.format(port))
httpd = socketserver.TCPServer(('0.0.0.0', port), Handler)
try:
    httpd.serve_forever()
except:
    print ("\nShutting down server..")
finally:
    httpd.shutdown()
    httpd.server_close()
