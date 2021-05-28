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
    res_data, err = DubboHandle.list(data.serviceName, data.methodName)
    if err:
        return res_400(msg=err)
    return res_200(data=res_data)


@router.post('/invoke', name='dubbo业务请求接口')
async def dubboInvoke(data: DubboInvokeBody):
    res_data, err = DubboHandle.invoke(data.serviceName, data.methodName, data.data)
    if err:
        return res_400(msg=err)
    return res_200(data=res_data)


@router.post('/search', name='dubbo服务搜索')
async def dubboSearch(body: DubboSearchBody):
    res_data, err = DubboHandle.search(body.serviceName)
    if err:
        return res_400(msg=err)
    return res_200(data=res_data)

