# -*- coding: UTF-8 -*-
'''
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/3/4 22:14
'''

from fastapi import APIRouter
from schemas import DubboListBody, DubboInvokeBody
from bm_dubbo import BmDubbo
import json

router = APIRouter()

@router.post('/dubboList', name='dubbo列表接口')
async def dubboList(data: DubboListBody):
    host = data.url.split(":")[0]
    port = data.url.split(":")[1]
    service_name = data.serviceName
    method_name = data.methodName
    conn = BmDubbo(host, port)
    status = conn.command("")
    #判断是否连接成功
    if status:
        #传入方法名，查询对应方法名的传值类型
        if method_name:
            param_data = conn.param_data(service_name, method_name)
            #判断方法是否存在
            if param_data:
                res_data = {'responseCode': 200, 'responseMsg': "请求成功"}
                dubbo_list = {'responseData': param_data}
                res_data.update(dubbo_list)
                return res_data
            #不存在返回报错
            else:
                return {'responseCode': 301, 'responseMsg': "找不到对应的serviceName"}
        #不传，直接返回服务下所有的数据
        else:
            response_data = conn.ls_invoke(service_name)
            if response_data:
                res_data = {'responseCode': 200, 'responseMsg': "请求成功"}
                dubbo_list = {'responseData':response_data}
                res_data.update(dubbo_list)
                return res_data
            else:
                return {'responseCode': 301, 'responseMsg': "找不到对应的serviceName"}

    #连接不成功返回报错
    else:
        return {'responseCode': 302, 'responseMsg': "dubbo服务连接出错"}


@router.post('/dubbo', name='dubbo业务请求接口')
async def dubboInvoke(data: DubboInvokeBody):
    host = data.url.split(":")[0]
    port = data.url.split(":")[1]
    service_name = data.serviceName
    method_name = data.methodName
    boby = data.data
    conn = BmDubbo(host, port)
    status = conn.command("")
    if status:
        # 根据服务名和方法名，返回param方法名和类型
        param_data = conn.param_data(service_name, method_name)
        if param_data:
            type = param_data['type']
            param = param_data['paramType']
            # 传参类型为枚举值方法
            if type == 0:
                l_data = [v for v in boby.values()]
                l_data = str(l_data)
                boby = l_data[1:-1]
            # 无需传参
            elif type == 1:
                boby = boby
            # 传参类型为集合对象
            elif type == 2:
                for k, v in boby.items():
                    if isinstance(v, list):
                        boby = v
                        break
            # 传参类型为自定义对象
            else:
                boby.update({"class": param})
            response_data = conn.invoke(service_name, method_name, boby)
            try:
                response_data = json.loads(response_data)
            except Exception as e:
                res_data = {'responseCode': 200, 'responseMsg': "请求成功"}
                res_data.update({'responseData':response_data})
                return res_data
            return response_data
        else:
            return {'responseCode': 301, 'responseMsg': "找不到对应的serviceName"}

    else:
        return {'responseCode': 302, 'responseMsg': "dubbo服务连接出错"}

