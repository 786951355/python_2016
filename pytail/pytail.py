#!/usr/bin/env python
# coding:utf-8

import os
import sys
import time
import argparse

parser = argparse.ArgumentParser(description = 'python tailf arguments')

parser.add_argument('-n', dest='number', nargs='?', const=10, help='e.g: -n 10, print least 10 lines ')
parser.add_argument('-f', dest='flush', action='store_true', help='print least lines')
parser.add_argument(dest='filename',metavar='filename')
args = parser.parse_args()

offset = -512
if args.number and os.path.exists(args.filename) and os.path.isfile(args.filename):
    while True:
        lst = []
        with open(args.filename,'rb') as f:
            fsize = os.stat(args.filename)
            if fsize.st_size <= -offset:
                f.seek(-fsize.st_size, 2)
                for line in f.readlines():
                    lst.append(line.decode().strip())
                if len(lst) <= int(args.number):
                    for i in lst:
                        print(i.strip(),)
                else:
                    for i in lst[-int(args.number):]:
                        print(i)
                break
            else:
                f.seek(offset,2)
                for line in f.readlines():
                    lst.append(line.decode())
                if len(lst) <= int(args.number):
                    offset *= 2
                else:
                    for i in lst[-int(args.number):]:
                        print(i.strip(),)
                    break
elif args.number is None and not args.flush and os.path.exists(args.filename) and os.path.isfile(args.filename):
    while True:
        lst = []
        with open(args.filename,'rb') as f:
            fsize = os.stat(args.filename)
            if fsize.st_size <= -offset:
                f.seek(-fsize.st_size, 2)
                for line in f.readlines():
                    lst.append(line.decode().strip())
                if len(lst) <= 10:
                    for i in lst:
                        print(i.strip(),)
                else:
                    for i in lst[-10:]:
                        print(i)
                break
            else:
                f.seek(offset,2)
                for line in f.readlines():
                    lst.append(line.decode())
                if len(lst) <= 10:
                    offset *= 2
                else:
                    for i in lst[-10:]:
                        print(i.strip(),)
                    break
elif args.flush and os.path.exists(args.filename) and os.path.isfile(args.filename):
    try:
        while True:
            lst = []
            with open(args.filename,'rb') as f:
                fsize = os.stat(args.filename)
                if fsize.st_size <= -offset:
                    f.seek(-fsize.st_size, 2)
                    for line in f.readlines():
                        lst.append(line.decode().strip())
                    if len(lst) <= 10:
                        for i in lst:
                            print(i.strip(),)
                    else:
                        for i in lst[-10:]:
                            print(i)
                    break
                else:
                    f.seek(offset,2)
                    for line in f.readlines():
                        lst.append(line.decode())
                    if len(lst) <= 10:
                        offset *= 2
                    else:
                        for i in lst[-10:]:
                            print(i.strip(),)
                        break
    
        with open(args.filename, 'rb') as f:
            f.seek(0,2)
            while True:
                offset = 0
                fsize = os.stat(args.filename)
                if offset >= fsize.st_size:
                    f.seek(0,2)
                for l in f.readlines():
                    if l:
                        print(l.decode().strip())
                f.seek(f.tell())
    except KeyboardInterrupt:
        pass
elif not os.path.exists(args.filename):
    print('文件不存在')
else:
    print('参数不是文件类型')