#!/usr/bin/python
#coding=utf-8

import socket

def ping(ip,port):
    normal = True
    try:
        conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        dest = (str(ip),int(port))
        conn.settimeout(1)
        status = conn.connect_ex(dest)
        if status != 0:
            normal = False
    except Exception ,e:
        normal = False
    return normal
