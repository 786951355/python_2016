#!/usr/bin/env python
#coding:utf-8

import os
import base64
import requests
import threading
from socketserver import BaseRequestHandler, ThreadingTCPServer


class MainHandler(BaseRequestHandler):
    def handle(self):
        datadir = '/log/'
        agents = {}
        host = '192.168.2.151:3000'
        url = 'http://{}/reciveagent'.format(host)
        while True:
            buffer = self.request.recv(1024)
            if not buffer:
                break
            if buffer.decode() == 'exit':
                if agents:
                    agents[self.client_address[0]] = []
                    requests.post(url, json=agents)
            else:
                decode_data = buffer.decode().split('::')
                filename = datadir + self.client_address[0] + base64.urlsafe_b64decode(decode_data[0]).decode()
                
                if self.client_address[0] in agents:
                     if filename not in agents[self.client_address[0]]:
                        agents[self.client_address[0]].append(filename)
                else:
                    agents[self.client_address[0]] = [filename]

                requests.post(url, json=agents)
                dirname = os.path.dirname(filename)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                with open(filename, 'a+') as f:
                     f.write(decode_data[1])

if __name__ == '__main__':
    try:
        Pools = 10
        address = ('0.0.0.0', 9000)
        server = ThreadingTCPServer(address, MainHandler)
        for i in range(Pools):
            t = threading.Thread(target=server.serve_forever, daemon=True)
            t.start()
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
