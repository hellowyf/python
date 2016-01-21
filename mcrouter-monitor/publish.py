#!/usr/bin/python
#coding=utf-8

import json
import redis
from package.ping import ping
from package.mc_redis import add_redis,del_redis


if __name__ == '__main__':
	file_url = "/usr/local/mcrouter/etc/mcrouter.conf"
	modified = 0
	redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
	try:
		len = redis_conn.llen('down_server')
		values = redis_conn.lrange('down_server',0,len-1)
	except Exception,e:
		print e
	if len > 0:
		with open(file_url,'r') as msg:
			msg_json = json.load(msg)
			server_list = msg_json['pools']['A']['servers']
		for value in values:
			server_ip = value.split(':')[0]
			server_port = value.split(':')[1]
			if ping(server_ip,server_port):
				server_list.append(value)
				modified += 1
				add_redis('up_server',value,redis_conn)
				del_redis('down_server',value,redis_conn)
		if modified != 0:
			msg_json["pools"]['A']['servers'] = server_list
			msg_modify = json.dumps(msg_json,sort_keys=True,indent=2)
			with open(file_url,'w') as modify:
				modify.write(msg_modify)
	
	
