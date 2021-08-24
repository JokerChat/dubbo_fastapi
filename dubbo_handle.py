# -*- coding: UTF-8 -*-
'''
@Project ：dubbo_fastapi
@File    ：dubbo_handle.py
@IDE     ：PyCharm 
@Author  ：junjie
@Date    ：2021/5/15 1:57 下午 
'''
from bm_dubbo import BmDubbo,GetDubboService
import json

class DubboHandle(object):

    @staticmethod
    def search(service_name):
        conn = GetDubboService()
        if conn.zk:
            data = conn.get_dubbo_info(service_name)
            return data, None
        else:
            return None, "zk服务连接失败"


    @staticmethod
    def list(service_name, method_name):
        zk_conn = GetDubboService()
        if zk_conn.zk:
            zk_data = zk_conn.get_dubbo_info(service_name)
            if zk_data:
                host, port = zk_data['url'].split(":")
                service_name = zk_data['interface']
                conn = BmDubbo(host, port)
                status = conn.command("")
                # 判断是否连接成功
                if status:
                    # 传入方法名，查询对应方法名的传值类型
                    if method_name:
                        param_data = conn.param_data(service_name, method_name)
                        # 判断方法是否存在
                        if param_data:
                            return param_data, None
                        # 不存在返回报错
                        else:
                            return None, f"{service_name.split('.')[-1]}服务下不存在{method_name}方法"
                    # 不传，直接返回服务下所有的数据
                    else:
                        response_data = conn.ls_invoke(service_name)
                        if response_data:
                            return response_data, None
                        else:
                            return None, f"{service_name}服务查询失败"

                # 连接不成功返回报错
                else:
                    return None, f"{service_name}服务连接出错"
            else:
                return None, f"{service_name}没有在zk中心注册"
        else:
            return None, "zk服务连接失败"



    @staticmethod
    def invoke(service_name, method_name, data):
        zk_conn = GetDubboService()
        if zk_conn.zk:
            zk_data = zk_conn.get_dubbo_info(service_name)
            if zk_data:
                host, port = zk_data['url'].split(":")
                service_name = zk_data['interface']
                boby = data.copy()
                conn = BmDubbo(host, port)
                status = conn.command("")
                if status:
                    # 根据服务名和方法名，返回param方法名和类型
                    param_data = conn.param_data(service_name, method_name)
                    if param_data:
                        type = param_data['type']
                        param = param_data['paramType']
                        # 传参类型为枚举值方法
                        if type == 0 and isinstance(boby, dict):
                            l_data = []
                            for v in  boby.values():
                                if isinstance(v,str):
                                    v = f"'{v}'"
                                elif isinstance(v,dict) or isinstance(v,list):
                                    v = json.dumps(v)
                                    v = f"'{v}'"
                                l_data.append(str(v))
                            boby = ','.join(l_data)
                        # 无需传参
                        elif type == 1:
                            boby = ''
                        # 传参类型为集合对象
                        elif type == 2:
                            # params 只有一个集合对象传参
                            if isinstance(boby, list):
                                boby = boby
                            # params 一个集合对象后面跟着多个枚举值
                            elif isinstance(boby, dict):
                                set_list = []
                                for v in boby.values():
                                    set_list.append(v)
                                set_data = str(set_list)
                                boby = set_data[1:-1]
                        # 传参类型为自定义对象
                        elif type == 3:
                            # 兼容多个自定义对象传参
                            if isinstance(param, list):
                                dtoList = []
                                for index, dto in enumerate(boby):
                                    dto.update({"class": param[index]})
                                    dtoList.append(json.dumps(dto))
                                boby = ','.join(dtoList)
                            elif isinstance(boby, dict):
                                boby.update({"class": param})
                                boby = json.dumps(boby)
                            else:
                                return None, f"data请求参数有误,请检查！"
                        else:
                            return None, f"data请求参数有误,请检查！"
                        response_data = conn.invoke(service_name, method_name, boby)
                        try:
                            response_data = json.loads(response_data)
                        except Exception as e:
                            return None, f"解析json失败:{response_data}"
                            # raise ControlException(f"解析json失败:{response_data},{str(response_data)}")
                        return response_data, None
                    else:
                        return None, f"{service_name.split('.')[-1]}服务下不存在{method_name}方法"
                else:
                    return None, f"{service_name}服务连接出错"
            else:
                return None, f"{service_name}没有在zk中心注册"
        else:
            return None, "zk服务连接失败"


