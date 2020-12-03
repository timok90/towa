import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from database import MySqliteDb
from datetime import datetime


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self):
        super().__init__()
        self.db = None

    def do_GET(self):
        # Log the data
        self._insert_logdata()

        if self.path == "/":
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

            # get the headers and ip adress of the client
            headers = self.headers
            client_address = self.get_ip_client()

            # create html code
            html = f"<html><head></head><body><h1>Hello {name}! {client_address}  and the headers: {headers}</h1></body></html>"

            # write the html code
            self.wfile.write(bytes(html, "utf8"))
        return None

    def _insert_logdata(self):
        log_data = self._get_logging_data()
        self.db._insert_logging_data(tablename=self.db.tablename,
                                     logging_data=log_data)
        return log_data

    def _get_logging_data(self) -> dict:
        """ Returns the data to log the client addressing the server"""
        # get the ip adress of the client
        user_ip = self.get_ip_client()
        timestamp = int(datetime.utcnow().timestamp())
        protocol = self.get_protocol()
        host = "host"
        path = "path"
        query = "query"

        log_data = {
            "user_ip": user_ip,
            "timestamp": timestamp,
            "protocol": protocol,
            "host": host,
            "path": path,
            "query": query
        }

        print(log_data)
        print(self.get_host())
        return log_data

    def get_ip_client(self):
        # get the ip adress of the client
        return self.client_address[0]

    def get_protocol(self):
        return self.protocol_version

    def get_host(self):
        return self.requestline


def myHttpServer():

    # create db
    db = MySqliteDb()
    db.create_logging_table("LoggingTable")

    # create the handler obj
    handler_object = MyHttpRequestHandler
    handler_object.db = db
    PORT = 8000

    with socketserver.TCPServer(("", PORT), handler_object) as myserver:
        # Start server
        myserver.serve_forever()


if __name__ == "__main__":
    myHttpServer()