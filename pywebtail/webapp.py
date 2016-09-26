#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import threading
from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

agents = {}
class LoadAgentHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode())
        for k in data:
            if data[k]:
                agents.update(data)
            else:
                agents.pop(k)


class MainHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class FlushAgentHandler(RequestHandler):
    def get(self):
        self.render('agent.html',title="web tail",header="客户端列表",books=agents)


class BodyHandler(RequestHandler):
    def get(self):
        self.render('tail.html')


class WebTailHandler(WebSocketHandler):
    fds = {}

    def initialize(self, tailer):
        self.tailer = tailer

    def shutdown(self):
        filename = self.fds.pop(self.ws_connection, None)
        if filename is not None:
            self.tailer.unregister(filename, Handler(self))

    def on_message(self, message):
        self.shutdown()
        self.tailer.register(message, Handler(self))
        self.fds[self.ws_connection] = message

    def on_connection_close(self):
        self.shutdown()
        super().on_connection_close()


class Handler:
    def __init__(self, handler):
        self.handler = handler

    def __hash__(self):
        return hash(self.handler.ws_connection)

    def __eq__(self, other):
        if not isinstance(other, Handler):
            return False
        return self.handler.ws_connection == other.handler.ws_connection

    def write_message(self, message, binary=False):
        self.handler.write_message(message, binary)


class Tailer:
    def __init__(self):
        self.files = {}
        self.events = {}

    def register(self, filename, handler):
        if filename not in self.files.keys():
            self.events[filename] = threading.Event()
            self.files[filename] = set()
            threading.Thread(name='tail-{}'.format(filename), target=self.worker,
                             args=(filename, self.events[filename]), daemon=True).start()
        self.files[filename].add(handler)

    def worker(self, filename, event):
        size = os.path.getsize(filename)
        while not event.is_set():
            with open(filename, 'r') as f:
                if size > os.path.getsize(filename):
                    size = 0
                f.seek(size)
                for line in f:
                    for handler in self.files[filename]:
                        handler.write_message(line)
                size = os.path.getsize(filename)
            event.wait(0.1)

    def unregister(self, filename, handler):
        handlers = self.files.get(filename, set())
        if handler in handlers:
            handlers.remove(handler)
        else:
            print('handler does not exist')
        self.files[filename] = handlers
        if len(handlers) <= 0:
            event = self.events.pop(filename)
            event.set()
            self.files.pop(filename)


if __name__ == '__main__':
    tailer = Tailer()
    app = Application(
        handlers = [(r'/', MainHandler),
                    (r'/tail',BodyHandler),
                    (r'/agent', FlushAgentHandler),
                    (r'/reciveagent',LoadAgentHandler),
                    (r'/ws', WebTailHandler, {'tailer': tailer})
                    ],
        template_path = os.path.join(os.path.dirname(__file__), "templates")
    )
    app.listen(3000)
    server = HTTPServer(app)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().stop()
