import http.server
import socketserver
import socket
from urllib.parse import urlparse, parse_qs
from database import MySqliteDb
from datetime import datetime
import json


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.serverAdress = ""

    def do_GET(self):
        # Log the data
        self._insert_logdata()
        query = parse_qs(urlparse(self.path).query)
        print(query)

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
        protocol = str(self.get_protocol())
        host = self.get_host()
        host = self.serverAdress
        path = urlparse(self.path).path
        query = json.dumps(parse_qs(urlparse(self.path).query))

        log_data = {
            "remote_ip": user_ip,
            "timestamp": timestamp,
            "protocol": protocol,
            "host": host,
            "path": path,
            "query": query
        }

        print(log_data)
        return log_data

    def get_ip_client(self):
        # get the ip adress of the client
        return self.client_address[0]

    def get_protocol(self):
        return self.protocol_version

    def get_host(self):
        return urlparse(self.path).netloc


def myHttpServer():

    # create db
    db = MySqliteDb()
    db.create_logging_table("LoggingTable")

    # create the handler obj
    handler_object = MyHttpRequestHandler
    handler_object.db = db
    PORT = 8000

    myserver = socketserver.TCPServer(("", PORT), handler_object)
    handler_object.serverAdress = myserver.server_address[0]
    print("server adress: ", myserver.server_address)
    myserver.serve_forever()


if __name__ == "__main__":
    myHttpServer()