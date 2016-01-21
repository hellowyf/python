#!/usr/bin/python
#coding=utf-8
from flask import Flask,request
import sys
import json
from package.ping import ping
from package.mc_redis import add_redis,del_redis,exist_in_redis,get_redis,get_redis_count
reload(sys)
sys.setdefaultencoding( "utf-8" )

mc = Flask(__name__)

@mc.route('/add')
def add_host():
	if 'ip' in request.args and 'port' in request.args:
		ip,port = request.args['ip'],request.args['port']
		host = ip + ':' + port
		add_redis('down_server',host)
		add_redis('new_server',host)
		return "Roger That! \n%s 已经写入" %host
	else:
		return "error msg!"

@mc.route('/del')
def del_host():
	if 'ip' in request.args and 'port' in request.args:
		ip,port = request.args['ip'],request.args['port']
		host = ip + ':' + port
		del_redis('up_server',host)
		del_redis('new_server',host)
		del_redis('down_server',host)
		return "Roger That! \n%s 已经删除" %host
	else:
		return "error msg!"

@mc.route('/get/<key>')
def get_host(key):
	values = get_redis(key)
	count = get_redis_count(key)
	redis_all = {'count': count,'server': values}
	return json.dumps(redis_all,sort_keys=True,indent=2)

if __name__ == "__main__":
	mc.run(host="0.0.0.0",port=8888,debug=True)
