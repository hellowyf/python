#!/usr/bin/python2.7
#coding=utf-8
'''
ec2_instace类对aws的ec2进行包装，方便获取ec2实例的ip，tagName等数据
get_instance_cpu函数根据传入的实例id，到cloudwatch中获取最近一周的cpu使用率信息.
'''

import boto.ec2.cloudwatch
import json
import ansible.runner
import datetime
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ec2_instance(object):
    
    def __init__(self,instance_id,conn=None):
        self.instance_id = instance_id
        if not conn:
            self.conn = boto.ec2.connect_to_region("cn-north-1")
        else:
            self.conn = conn

    @property
    def private_ip_address(self):
       return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].private_ip_address
    
    @property
    def public_ip_address(self):
        return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].ip_address

    @property
    def instance_type(self):
        return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].instance_type

    @property
    def root_device_name(self):
        return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].root_device_name

    @property
    def block_device_mapping(self):
        return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].block_device_mapping
    @property
    def ec2_tag_name(self):
        return self.conn.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].tags['Name']


def get_instance_cpu(instance_id,recent_hours=168,conn=None):
    instance_id = instance_id
    recent_hours = recent_hours
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(hours=recent_hours)
    period = recent_hours*3600/1440
    if not conn:
        conn = boto.ec2.cloudwatch.connect_to_region("cn-north-1")
    dims = {'InstanceId':instance_id}
    metrics = conn.get_metric_statistics(period,start,end,"CPUUtilization","AWS/EC2",['Average', 'Maximum', 'Minimum'],dims)
    if metrics:
        max_val = max(m['Maximum'] for m in metrics)
        min_val = min(m['Minimum'] for m in metrics)
        avg_val = '%.2f' %(sum(m['Average'] for m in metrics)/float(len(metrics)))
        cpu_dict = {'max':max_val,'min':min_val,'avg':avg_val}
    else:
        cpu_dict = {'max':'N/A','min':'N/A','avg':'N/A'}
    return cpu_dict

