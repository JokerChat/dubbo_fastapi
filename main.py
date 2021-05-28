# -*- coding: UTF-8 -*-
'''
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/3/4 22:14
'''

import uvicorn
from fastapi import FastAPI
from dubbo_routers import router
app = FastAPI()

app.include_router(router, prefix="/api/dubbo", tags=["dubbo接口相关"])

if __name__ == "__main__":
    #reload 修改后自动重载
    #debug  开启debug模式
    uvicorn.run(app='main:app', host="0.0.0.0",port=5000,reload=True,debug=True)