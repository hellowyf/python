#!/usr/bin/python
from .ec2_connection import ec2_instance , get_instance_cpu
from .get_fact import get_instance_disk,get_instance_mem

__all__ = [
    ec2_instance,
    get_instance_cpu,
    get_instance_disk,
    get_instance_mem
]
