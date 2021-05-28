# -*- coding: UTF-8 -*-
'''
@IDE     ：PyCharm
@Author  ：junjie
@Date    ：2021/5/4 22:14
'''

#从源项目抽出来，配置信息暂不用yaml管理

#这里配置ZK注册中心的地址
ENV = 'test'

zk_config = {
    "test": ['xxxxx:2181','xxxxx:2182','xxx:2183'],
    "dev":['xxxxx:2181','xxxxx:2182','xxx:2183'],
}

if ENV =='test':
    ZK_CONFIG = zk_config['test']

elif ENV =='dev':
    ZK_CONFIG = zk_config['dev']