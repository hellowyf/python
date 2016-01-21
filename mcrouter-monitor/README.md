#mcrouter
	mcrouter配置文件动态添加、删除不可用服务器；

##publish.py
	从redis的downserver队列中获取ip信息，如果不为空，就探测此ip和端口
	如果ip和端口通，将ip从downserver中删除，写入upserver，并写入mcrouter配置文件

##unpublish.py
	从mcrouter配置文件获取IP和端口数据
	探测ip和端口
	如果端口不通，将ip从配置文件中删除
	并将次ip从redis的upserver迁移到downserver


#web.py
	web接口用于新加或删除服务器

## /add
	http://$ip/add?ip=xxx&port=xxx
	将ip/port对写入down_server的redis队列

## /del
	http://$ip/del?ip=xxx&port=xxx
	将ip/port对从redis队列中删除

##/get
	http://$ip/get/$key
	从redis中获取指定key的数据
