#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        #decode into string
        data_to_string = self.data.decode('utf-8')

        #first line
        first_line = data_to_string.split('\r\n')[0]

        #first word
        first_word = first_line.split(' ')[0]

        #second word
        second_word = first_line.split(' ')[1]

        #405 Method Not Allowed
        #make html
        path = ' '

        if first_word == "GET":
            if "css" not in second_word:
                if "index.html" not in second_word:
                    if second_word[-1] == "/":
                        second_word = second_word + "index.html"
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + second_word +'/','utf-8'))
                        return 0
            path = "./www" + second_word
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed",'utf-8'))
            return 0

        if ".html" in second_word:
            self.Test_web_server(path,"text/html")
        elif ".css" in second_word:
            self.Test_web_server(path,"text/css")


    def Test_web_server(self,path,type):
        #print("path: ",path)
        if os.path.exists(path):
           file = open(path,'r')
           data = file.read()
           #print("200",type)
           self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" +type +"\r\n"  +"\r\n\r\n"+data,'utf-8'))
           return 0
        else:
            #print("404")
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Not Found",'utf-8'))
            return 0

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
