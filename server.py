from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import cgi
PORT = 8000  
IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER): ## isse toh image folder create hoga agr exist ni krta
    os.makedirs(IMAGE_FOLDER)
class SimpleHandler(BaseHTTPRequestHandler):  #yeah toh get or post k liye h
    def do_GET(self):
        if self.path == '/':
            with open("form.html", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        elif self.path.startswith("/images/"):
            filepath = self.path[1:]
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File Not Found")
    def do_POST(self):
        if self.path == '/submit':
             
            # content_type=self.headers['Content-Type']
            # if not content_type or not content_type.startswith('multipart/form-data'):
            #     self.send_error(400,"Bad Request Only multipart/form-data is supported")
            #     return
            # ctype,pdict=cgi.FieldStorage(fp=self.rfile,haders=self.headers,environ={'REQUEST_METHOD':'POST'})
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))   #yeah toh basically read krta forms ki field ko, inputs ko
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                pdict['CONTENT-LENGTH'] = int(self.headers.get('Content-length'))
                fields = cgi.parse_multipart(self.rfile, pdict)
                fname = fields.get('fname', [''])[0]
                lname = fields.get('lname', [''])[0]
                email = fields.get('email', [''])[0]
                sports = fields.get('sports', [''])[0]
                gender = fields.get('gender', [''])[0]
                hobbies = fields.get('hobbies', [])
                message = fields.get('message', [''])[0]
                fileitem = fields.get('image', [b''])[0]
                filename = f"{int(time.time())}.jpg"
                filepath = os.path.join(IMAGE_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(fileitem)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"""
                    <html><body>
                    <h2>Form Submitted Successfully</h2>
                    <p>Name: {fname} {lname}</p>
                    <p>Email: {email}</p>
                    <p>Gender: {gender}</p>
                    <p>Sports: {sports}</p>
                    <p>Hobbies: {', '.join(hobbies)}</p>
                    <p>Message: {message}</p>
                    <p>Image saved as: {filename}</p>
                    <img src="/images/{filename}" width="200">
                    </body></html>
                """.encode())

def run():
    host = 'localhost'
    port = PORT
    server_address = (host, port)
    server = HTTPServer(server_address, SimpleHandler)
    print(f"Server started on http://{host}:{port}")
    server.serve_forever()

#     def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8658):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print(f'Starting server on port {port}...')
#     httpd.serve_forever()
# def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
#     server_address = ('0.0.0.0', port)
#     httpd = server_class(server_address, handler_class)
#     print(f'Starting server on port {port}...')
#     httpd.serve_forever()

if __name__ == "__main__":
    run()