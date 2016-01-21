#!/usr/bin/python
#coding=utf-8

import json
import socket
import redis
from package.ping import ping
from package.mc_redis import add_redis,del_redis 


if __name__ == '__main__':
	file_url = "/usr/local/mcrouter/etc/mcrouter.conf"
	modified = 0
	with open(file_url,'r') as msg:
		msg_json = json.load(msg)
		server_list = msg_json["pools"]["A"]['servers']
	redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
	for server in server_list:
		server_ip = server.split(':')[0]
		server_port = server.split(':')[1]
		if not ping(server_ip,server_port):
			server_list.remove(server)
			add_redis('down_server',server,redis_conn)	
			del_redis('up_server',server,redis_conn)
			modified += 1
		else:
			add_redis('up_server',server,redis_conn)
	if modified != 0:
		msg_json["pools"]["A"]['servers'] = server_list
		msg_modify = json.dumps(msg_json,sort_keys=True,indent=2)
		with open(file_url,'w') as modify:
			modify.write(msg_modify)

