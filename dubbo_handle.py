# -*- coding: UTF-8 -*-
'''
@Project ：dubbo_fastapi
@File    ：dubbo_handle.py
@IDE     ：PyCharm 
@Author  ：junjie
@Date    ：2021/5/15 1:57 下午 
'''
from dubborequests import Config
from config import ZK_CONFIG
import dubborequests

class DubboHandle(object):

    Config.zookeeper_url_list = ZK_CONFIG

    @staticmethod
    def search(service_name):
        service_info = dubborequests.search(service_name)
        return service_info

    @staticmethod
    def list(service_name, method_name=None):
        list_data = dubborequests.list(service_name, method_name)
        return list_data

    @staticmethod
    def invoke(service_name, method_name, data):
        res_data = dubborequests.zk_invoke(service_name, method_name, data)
        return res_data['invoke_data']


    @staticmethod
    def telnet_list(ip, port, service_name, method_name=None):
        list_data = dubborequests.telnet_list(ip, port, service_name, method_name)
        return list_data


