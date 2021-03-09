# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2020/11/29 21:12
# @FileName     :bm_dubbo.py
# @Motto        :ABC
#IDE            :PyCharm

import telnetlib

import json

import re

class BmDubbo():

    prompt = 'dubbo>'

    def __init__(self, host, port):
        self.conn = self.conn(host, port)

    def conn(self,host, port):
        conn = telnetlib.Telnet()
        try:
            conn.open(host, port, timeout=1)
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
        if isinstance(arg, dict) and arg:
            command_str = "invoke {0}.{1}({2})".format(
                service_name, method_name, json.dumps(arg))
        elif isinstance(arg, list) and arg:
            command_str = "invoke {0}.{1}({2})".format(
                service_name, method_name, json.dumps(arg))
        elif isinstance(arg, dict) and not arg:
            command_str = "invoke {0}.{1}()".format(
                service_name, method_name)
        else:
            command_str = "invoke {0}.{1}(11{2})".format(
                service_name, method_name, arg)
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



if __name__ == '__main__':
    conn = BmDubbo('ip地址', '端口')
    data_ = conn.ls_invoke("服务名")
    print(data_)
