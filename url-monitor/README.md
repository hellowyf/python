#url-monitor

	url监控报警，脚本＋crontab一起使用，

##url-monitor.py

	读取host.json和url.json文件，迭代serverip和url接口，针对每个server的每个接口进行请求监控，返回状态码错误或者响应的数据不正确，进行报警，并将错误的server/url对写入error文件

##recover.py
	读取error.json文件，对文件中的错误接口进行监控请求，如果请求正常，server/url对从error文件删除并邮件通知回复。	
