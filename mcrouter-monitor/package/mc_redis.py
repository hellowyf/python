#!/usr/bin/python
#coding=utf-8

import json
import redis

def add_redis(key,value,redis_conn=None):
    if not redis_conn:
        redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
    try:
        if not exist_in_redis(key,value,redis_conn):
            redis_conn.lpush(key,value)
    except Exception,e:
        print e

def del_redis(key,value,redis_conn=None):
    if not redis_conn:
        redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
    try:
        if exist_in_redis(key,value,redis_conn):
            redis_conn.lrem(key,0,value)
    except Exception,e:
        print e

def exist_in_redis(key,value,redis_conn=None):
    if not redis_conn:
        redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
    try:
        len = redis_conn.llen(key)
        values = redis_conn.lrange(key,0,len-1)
    except Exception,e:
        print e
    if value in values:
        return True
    else:
        return False

def get_redis(key,redis_conn=None):
    	if not redis_conn:
		redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
	try:
		len = redis_conn.llen(key)
		values = redis_conn.lrange(key,0,len-1)
		return values
	except Exception,e:
		print e

def get_redis_count(key,redis_conn=None):
	if not redis_conn:
		redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379)
	try:
		len = redis_conn.llen(key)
		return len
	except Exception,e:
		print e
