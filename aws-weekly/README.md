#aws服务器状态周报
	通过cloudwatch获取服务器的cpu状态，取出最近一周的峰值，平均值和最小值
	通过ansible的setup模块，获取机器的磁盘使用和内存使用情况
	并生成为html的表格，发送邮件
