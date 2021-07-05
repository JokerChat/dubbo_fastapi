# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2020/11/29 21:12
# @FileName     :bm_dubbo.py
# @Motto        :ABC
#IDE            :PyCharm

import telnetlib
import json
import re
from kazoo.client import KazooClient
from urllib import parse
from config import ZK_CONFIG


class BmDubbo(object):

    prompt = 'dubbo>'

    def __init__(self, host, port):
        self.conn = self.conn(host, port)

    def conn(self,host, port):
        conn = telnetlib.Telnet()
        try:
            #3秒后 连接超时
            conn.open(host, port, timeout=3)
        except BaseException:
            return False
        return conn


    def command(self, str_=""):
        # 模拟cmd控制台 dubbo>invoke ...
        if self.conn :
            self.conn.write(str_.encode() + b'\n')
            data = self.conn.read_until(self.prompt.encode())
            return data
        else:
            return False

    def invoke(self, service_name, method_name, arg):
        command_str = "invoke {0}.{1}({2})".format(service_name, method_name, arg)
        data = self.command(command_str)
        try:
            # 字节数据解码 utf8
            data = data.decode("utf-8").split('\n')[0].strip()
        except BaseException:
            # 字节数据解码 gbk
            data = data.decode("gbk").split('\n')[0].strip()
        return data

    def ls_invoke(self, service_name):
        command_str = "ls -l {0}".format(service_name)
        data = self.command(command_str)
        if "No such service" in data.decode("utf-8"):
            return False
        else:
            data = data.decode("utf-8").split('\n')
            key = ['methodName', 'paramType','type']
            dubbo_list = []
            for i in range(0, len(data) - 1):
                value = []
                dubbo_name = data[i].strip().split(' ')[1]
                method_name = re.findall(r"(.*?)[(]", dubbo_name)[0]
                value.append(method_name)
                paramType = re.findall(r"[(](.*?)[)]", dubbo_name)[0]
                paramTypeList = paramType.split(',')
                if len(paramTypeList) ==1:
                    paramTypeList = paramTypeList[0]
                value.append(paramTypeList)
                if 'java.lang' in paramType or 'java.math' in paramType:
                    value.append(0)
                elif not paramType:
                    value.append(1)
                elif 'List' in paramType:
                    value.append(2)
                else:
                    value.append(3)
                dubbo_list.append(dict(zip(key, value)))
            return dubbo_list

    def param_data(self,service_name,method_name):
        dubbo_data = self.ls_invoke(service_name)
        if dubbo_data:
            dubbo_list = dubbo_data
            if dubbo_list:
                for i in dubbo_list:
                    for v in i.values():
                        if v == method_name:
                            param_key = ['paramType','type']
                            param_value = [i.get('paramType'),i.get('type')]
                            return dict(zip(param_key,param_value))
            else:
                return False
        else:
            return False


class GetDubboService(object):
    def __init__(self):

        self.hosts = ZK_CONFIG
        self.zk = self.zk_conn()

    def zk_conn(self):
        try:
            zk = KazooClient(hosts=self.hosts, timeout=2)
            zk.start(2)  # 与zookeeper连接
        except BaseException as e:
            print(str(e))
            return False
        return zk

    def get_dubbo_info(self, dubbo_service):
        dubbo_service_data = {}
        try:
            #先查出注册中心所有的dubbo服务
            all_node = self.zk.get_children('/dubbo')
            #根据传入服务名匹配对应的服务
            node = [i for i in all_node if dubbo_service in i]
            # 查询dubbo服务的详细信息
            #遍历数据，过滤掉空数据
            for i in node:
                if self.zk.get_children(f'/dubbo/{i}/providers'):
                    dubbo_data = self.zk.get_children(f'/dubbo/{i}/providers')
                    for index, a in enumerate(dubbo_data):
                        url = parse.urlparse(parse.unquote(a)).netloc
                        host, port = url.split(":")
                        conn = BmDubbo(host, port)
                        status = conn.command("")
                        if status:
                            data = dubbo_data[index]
                            break
            self.zk.stop()
        except BaseException as e:
            return dubbo_service_data
        #parse.unquote 解码
        #parse.urlparse 解析URL
        #parse.query 获取查询参数
        #parse.parse_qsl 返回列表
        url_data = parse.urlparse(parse.unquote(data))
        query_data = dict(parse.parse_qsl(url_data.query))
        query_data['methods'] = query_data['methods'].split(",")
        dubbo_service_data['url'] = url_data.netloc
        dubbo_service_data['dubbo_service'] = dubbo_service
        dubbo_service_data.update(query_data)
        return dubbo_service_data



if __name__ == '__main__':
    conn1 = GetDubboService()
    if conn1.zk:
        data = conn1.get_dubbo_info('xxx')
        print(json.dumps(data))
    else:
        print("连接zk服务异常")
