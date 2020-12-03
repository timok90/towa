import http.server
import socketserver


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/index":
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# create the handler obj
handler_object = MyHttpRequestHandler

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler
myserver = socketserver.TCPServer(("", PORT), handler)

# Start server
myserver.serve_forever()