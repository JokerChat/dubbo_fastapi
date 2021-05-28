# -*- coding: UTF-8 -*-
'''
@Project ：dubbo_fastapi
@File    ：ResponseNormal.py
@IDE     ：PyCharm 
@Author  ：junjie
@Date    ：2021/3/2 21:15 
'''
from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union
from fastapi.encoders import jsonable_encoder

#* 后面的参数被视为关键字参数。在函数调用时，关键字参数必须传入参数名
#-> Response 代表函数返回的是一个外部可访问的类的私有变量
def res_200(*, data: Union[list, dict, str,None]) -> Response:
    content = {
        'responseCode': 200,
        'responseMsg': "请求成功",
        'responseData': data,
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(content)
    )

def res_400(*, msg : str="系统异常")-> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'responseCode': 400,
            'responseMsg': msg
        }
    )