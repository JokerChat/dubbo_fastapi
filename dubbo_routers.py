# -*- coding: UTF-8 -*-
'''
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/3/4 22:14
'''

from fastapi import APIRouter
from schemas import DubboListBody, DubboInvokeBody,DubboSearchBody
from dubbo_handle import DubboHandle
from ResponseNormal import res_200,res_400

router = APIRouter()

@router.post('/list', name='dubbo列表接口')
async def dubboList(data: DubboListBody):
    try:
        res_data = DubboHandle.list(data.serviceName, data.methodName)
        return res_200(data=res_data)
    except Exception as e:
        return res_400(msg=str(e))




@router.post('/invoke', name='dubbo业务请求接口')
async def dubboInvoke(data: DubboInvokeBody):
    try:
        res_data = DubboHandle.invoke(data.serviceName, data.methodName, data.data)
        return res_data
    except Exception as e:
        return res_400(msg=str(e))


@router.post('/search', name='dubbo服务搜索')
async def dubboSearch(body: DubboSearchBody):
    try:
        res_data = DubboHandle.search(body.serviceName)
        return res_200(data=res_data)
    except Exception as e:
        return res_400(msg=str(e))

