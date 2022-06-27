import socketserver
import http.server
import urllib.request
import os
import time

PORT = 9098

class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

     url=""

     if "/songs/" in self.path:
       url=f"https://stream-cdn.gaana.com/{self.path[1:]}"
     elif "/hls/" in self.path:
       url = f"https://vodhlsgaana.akamaized.net/{self.path[1:]}"
     elif "/gn_img/" in self.path or "/images/" in self.path:
       url = f"https://a10.gaanacdn.com/{self.path[1:]}"
     else:
      return

     print(url)

     self.send_response(200)
     self.end_headers()
     return self.copyfile(urllib.request.urlopen(url), self.wfile)

try:
  httpd = socketserver.ForkingTCPServer(('', PORT), MyProxy)
  print ("Now serving at", str(PORT))
  httpd.serve_forever()
except KeyboardInterrupt:
  socketserver.socket.close(1)

