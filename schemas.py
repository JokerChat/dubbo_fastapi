# -*- coding: UTF-8 -*-
'''
@Project ：bmTest_fastapi
@File    ：dubbo_schemas.py
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/3/4 22:17
'''

from pydantic import BaseModel,validator,Field
from typing import Optional
import re
#创建数据模型
class DubboListBody(BaseModel):
    url : str = Field(..., title="dubbo接口IP地址",description="必传，格式为IP:端口")
    serviceName :str=Field(..., title="dubbo接口服务名",description="必传")
    methodName :str=Field(None, title="dubbo接口方法名",description="不传方法名查全部，否则查对应方法名下的传值类型")
    @validator('url','serviceName')
    def checkEmpty(cls,value):
        if value =='':
            raise ValueError('必须有值')
        return value

    @validator('url')
    def checkFormat(cls, value):
        result = re.match(r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5]):\d{0,5}', value)
        if not result:
            raise ValueError('不符合格式')
        return value


#继承DubboListBody模型，提高复用性
class DubboInvokeBody(DubboListBody):
    methodName : str
    data : dict
    @validator('methodName')
    def checkEmpty(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return value