#!/usr/bin/python2.7
#coding=utf-8

#from instance import ec2_connection
#from instance import get_fact 

from pyh import *
from instance.ec2_connection import ec2_instance , get_instance_cpu
from instance.get_fact import get_instance_disk,get_instance_mem

import boto.ec2
import boto.ec2.cloudwatch
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


"""
根据提供的aws标签的k/v，获取实例的id列表
"""
def get_instance_id(tag_key,tag_value,conn=None):
    if not conn:
        conn = boto.ec2.connect_to_region("cn-north-1")
        if not conn:
            print "connection error!"
    key = "tag:%s" % tag_key
    reservations = conn.get_all_instances(filters={key:tag_value,"instance-state-name": "running"})
    instances = [i for r in reservations for i in r.instances]
    instances_id = []
    for i in instances:
        instances_id.append(str(i)[9:])
    return instances_id


'''
主函数，实现机器列表获取和监控数据的获取，并生成html
'''

if __name__ == '__main__':
    input_get = sys.argv[1]
    key = input_get.split('=')[0]
    value = input_get.split('=')[1]
    instance_id_list = get_instance_id(key,value)
    if len(instance_id_list) == 0:
        exit(1)
    t = table(border="1",cl="table1",cellpadding="0",cellspacing="0")
    t<<tr(td('Name')+td('IP')+td('Type')+td('cpu_max')+td('cpu_min')+td('cpu_avg')+td('mem_usg')+td('disk'))
    for instance_id in instance_id_list:
        instance = ec2_instance(instance_id)
        instance_cpu = get_instance_cpu(instance_id)  #获取实例cpu数据
        instance_mem = get_instance_mem(instance.private_ip_address)  #根据ip获取内存信息
        instance_disk = get_instance_disk(instance.private_ip_address) #根据ip获取磁盘信息
        instance_tr = t << tr()
        instance_tr<<td(instance.ec2_tag_name)+td(instance.private_ip_address)+td(instance.instance_type)+td(instance_cpu['max'])+td(instance_cpu['min'])+td(instance_cpu['avg'])+td(instance_mem['usage'])
        for disk in instance_disk:
            instance_tr<<td({disk:instance_disk[disk]['usage']})
    page=PyH('OPS')
    page<<h1('AWS-服务器数据周报',align='center')
    page<<t
    page.printOut()
