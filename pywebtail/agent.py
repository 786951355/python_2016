#!/usr/bin/env python
#coding:utf-8

import os
import time
import base64
import signal
import threading
from socket import socket, AF_INET, SOCK_STREAM


all_file= ['/tmp/test.log','/tmp/hello.log','/tmp/1']
thread_list = []
host = '192.168.2.151'
port = 9000

s = socket(AF_INET, SOCK_STREAM)
connect_status = s.connect_ex((host, port))

def send_data(filename):
    try:
        with open(filename, 'rb') as f:
            f.seek(0,2)
            while True:
                offset = 0
                fsize = os.stat(filename)
                if offset >= fsize.st_size:
                    f.seek(0,2)
                for l in f.readlines():
                    if l:
                        s.send(base64.urlsafe_b64encode(filename.encode())+'::'.encode()+l)
                time.sleep(0.05)
                f.seek(f.tell())
    except FileNotFoundError as e:
        print("file not found")
    except OSError:
        pass
    except KeyboardInterrupt:
        s.close()


def handle(signum, frame):
    s.send(b'exit')
    s.close()
    os.abort()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle)
    if connect_status == 0:
        try:
            for f in all_file:
                t = threading.Thread(target=send_data,args=(f,))
                thread_list.append(t)
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
        except OSError:
            pass
        except KeyboardInterrupt:
            s.send(b'exit')
            s.close()
        finally:
            s.close()
    else:
        print('connect server failed!')
