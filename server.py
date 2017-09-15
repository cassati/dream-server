import http.server
import urllib.parse
import json
import task


class MyHttpHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        obj = {'status': 'error', 'message': 'method not allowed'}
        jsonstr = json.dumps(obj)
        self.send_response(400)
        self.end_headers()
        self.wfile.write(jsonstr.encode("utf-8"))
        self.wfile.flush()
        return

    def do_POST(self):
        # receive
        requestpath = urllib.parse.urlparse(self.path)
        length = int(self.headers.get('content-length', ""))
        bytedata = self.rfile.read(length)
        data = bytedata.decode("utf-8")

        # process request
        try:
            result = task.dispatch(requestpath.path, data, self)
            obj = {'status': 'success', 'message': result}
        except Exception as e:
            result = 'exception occur: ' + e.message
            obj = {'status': 'error', 'message': result}

        # send response
        jsonstr = json.dumps(obj)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(jsonstr.encode("utf-8"))
        self.wfile.flush()
        return


def start(ip, port):
    task.init()
    server_address = (ip, port)
    httpd = http.server.HTTPServer(server_address, MyHttpHandler)
    httpd.serve_forever()
