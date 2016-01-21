#!/usr/bin/python
#!coding=utf-8
'''
使用ansible的setup模块获取服务器的磁盘和内存使用情况
'''

import ansible.runner

def get_instance_disk(server_ip,host=None):
    if not host:
        host = '/tmp/host.yml'
    results = ansible.runner.Runner(host_list=host,pattern=server_ip,module_name='setup',module_args='filter=ansible_mounts').run()
    instance_disk = {}
    for server,result in results['contacted'].items():
        mounts = result['ansible_facts']['ansible_mounts']
        for device in mounts:
            disk_total = device['size_total']/1048576
            disk_availe = device['size_available']/1048576
            disk_usg = '%.2f' %((disk_total - disk_availe)/float(disk_total))
            disk = device['device']
            instance_disk.update({disk:{"total":disk_total,"available":disk_availe,"usage":disk_usg}})
    return instance_disk
            
def get_instance_mem(server_ip,host=None):
    if not host:
        host = '/tmp/host.yml'
    results = ansible.runner.Runner(host_list=host,pattern=server_ip,module_name='setup',module_args='filter=ansible_memory_mb').run()
    instance_mem = {}
    for server,result in results['contacted'].items():
        memory = result['ansible_facts']['ansible_memory_mb']['real']
        memory_free = memory['free']
        memory_total = memory['total']
        memory_used = memory['used']
        memory_usage = '%.2f' %(memory_used/float(memory_total))
        instance_mem.update({'total':memory_total,'free':memory_free,'used':memory_used,'usage':memory_usage})
    if instance_mem == {}:
        instance_mem.update({'total':'N/A','free':'N/A','used':'N/A','usage':'N/A'})
    return instance_mem
    
