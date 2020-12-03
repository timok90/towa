import http.server
import socketserver
from urllib.parse import urlparse, parse_qs


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        #send ok response
        self.send_response(200)

        # setting the header
        self.send_header("Content-type", "text/html")

        self.end_headers()

        # extract query params
        name = 'World'
        query_components = parse_qs(urlparse(self.path).query)
        if 'name' in query_components:
            name = query_components['name'][0]

        # get the ip adress of the client
        client_address = self.client_address[0]

        headers = self.headers

        # create html code
        html = f"<html><head></head><body><h1>Hello {name}! {client_address}  and the headers: {headers}</h1></body></html>"

        # write the html code
        self.wfile.write(bytes(html, "utf8"))
        return None


# create the handler obj
handler_object = MyHttpRequestHandler

PORT = 8000

with socketserver.TCPServer(("", PORT), handler_object) as myserver:
    # Start server
    myserver.serve_forever()