
# -*- coding: UTF-8 -*-
'''
@Project ：bmTest_fastapi
@File    ：dubbo_schemas.py
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/3/4 22:17
'''

from pydantic import BaseModel,validator,Field
from typing import Union
#创建数据模型
class DubboListBody(BaseModel):
    serviceName :str=Field(..., title="dubbo接口服务名",description="必传")
    methodName :str=Field(None, title="dubbo接口方法名",description="不传方法名查全部，否则查对应方法名下的传值类型")
    @validator('serviceName')
    def checkEmpty(cls,value):
        if value =='':
            raise ValueError('必须有值')
        return value



#继承DubboListBody模型，提高复用性
class DubboInvokeBody(DubboListBody):
    methodName : str
    data : Union[dict,list]
    @validator('methodName')
    def checkEmpty(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return value

class DubboSearchBody(BaseModel):
    serviceName :str=Field(..., title="dubbo服务名",description="必传")
    @validator('serviceName')
    def checkEmpty(cls,value):
        if value =='':
            raise ValueError('必须有值')
        return value