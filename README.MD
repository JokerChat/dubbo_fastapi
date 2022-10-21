## 使用方法
- pip install requirements.txt
- config.py 文件配置上你的zookeeper地址
- 右键运行main文件
- 访问http://127.0.0.1:5000/api/dubbo/xxx 即可开始测试dubbo接口
- 具体传参可看下面的dubbo接口文档
- 基于fastapi,将dubbo接口转换成便捷的http接口测试
- dockerFile部署,直接`docker build -t xx:xx .`

-----------------------------------------------------------
# 基于http协议dubbo接口文档

> 原理：基于python  telnetlib库，模拟Telnet命令进行dubbo接口测试，再封装成http接口
>
> 备注：部署的服务，必须可以连接上dubbo服务主机

## 前言

### 修改记录

| 编号 | 修改日期 | 修改内容 | 修改人 |
| ---- | -------- | -------- | ------ |
| 1    | 2021-3-9 | 创建文档 | Fang   |
| 2    | 2022-3-23 | 更新文档 |   Fang |
| 3 | 2022-10-21 | 新增`支持调用同一服务名，不同版本的dubbo服务` | Fang |

### 服务地址

测试环境：http://xxx.xx.xx.xx:5000

 ## 接口说明

 ### 1）查询服务名下的所有方法

**接口地址**

- 说明：根据dubbo接口地址和dubbo接口服务名，查询服务名下的所有方法
- 地址：`/api/dubbo/list`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                                                 |
| ---- | ----------- | ------ | ---------------------------------------------------- |
| 1    | serviceName | String | 服务名                                               |
| 2    | methodName  | String | 非必传，查询服务名下指定方法名的传值类型，不传查所有 |
| 3    | version     | String | 非必传，传值时查询指定版本号的服务                   |

**请求体示例**

```json
{
  "serviceName": "string",
  "methodName": "string",
  "version": "2.0.0"
}
```

**返回体**

| 序号 | 键值         | 类型   | 说明         |
| ---- | ------------ | ------ | :----------- |
| 1    | responseCode | Int    | 返回code     |
| 2    | responseMsg  | String | 返回信息     |
| 3    | responseData | Array  | data数组     |
| 4    | - param_type  | Array  | 方法传值类型 |
|      | - method | String | 方法名       |

**返回值示例（成功）**

```json
{
  "responseCode": 0,
  "responseMsg": "请求成功",
  "responseData": [
    {
      "method": "queryProductStoreInfo",
      "param_type": [
        "cn.com.xxxx.mallerp.dto.store.ProductStoreQueryRequest"
      ]
    }
  ]
}
```

**返回值示例（失败）**

```json
{
    "responseCode": 400,
    "responseMsg": "相应的异常信息"
}
```



### 2）dubbo接口-业务接口

**接口地址**

- 说明：根据dubbo接口地址和dubbo接口服务名，方法名，参数值实现dubbo接口逻辑
- 地址：`/api/dubbo/invoke`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                    |
| ---- | ----------- | ------ | ----------------------- |
| 1    | serviceName | string | 服务名                  |
| 2    | methodName  | string | 方法名                  |
| 3    | data        | object | 可看以下示例 |
| 4 | version | string | 非必传，传值时调用指定版本号的服务 |

**请求体示例1 -- 原生对象或者自定义对象传参**(**xxDto、jsonObj、java.util.HashMap**)

```json
{
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx",
    "methodName": "xxxxxx",
    "data": {
        "dto1": {
            "productStoreQueryDTOS": [
                {
                    "productNoNumDTOList": [
                        {
                            "num": 13,
                            "productNo": "10000620"
                        },
                        {
                            "num": 13,
                            "productNo": "10000014"
                        }
                    ],
                    "storeCode": "4401S1389"
                }
            ]
        }
    }
}
```
**请求体示例2 -- 枚举值类型传参**(**java.lang.String、java.lang.Integer**)

```json
{
    "serviceName": "xxxx",
    "methodName": "xxxxx",
    "data": {         //格式为json，枚举值顺序必须按照dubbo接口定义的传参顺序，注意是否为int还是string
        "account":"123456",
        "password":"3fd6ebe43dab8b6ce6d033a5da6e6ac5"
    }
}
```

**请求体示例3 -- 方法名无需传参**

```json
{
    "serviceName": "xxxx",
    "methodName": "xxxxxx",
    "data":{}      //传入空对象
}
```

**请求体示例4 --集合对象传参**(**java.util.List**)

```json
{
    "serviceName": "xxxx",
    "methodName": "xxxxxx",
    "data":{
        "empList": [
            "30000445",
            "30000444"
        ]
    } //传入对象，里面嵌套数组
}
```

**请求体示例5 --集合对象传参,后面跟着枚举值**(**java.util.List 、 java.lang.String 、 java.lang.String**)

```json
{
    "serviceName": "xxxx",
    "methodName": "xxxxxx",
    "data":{
        "userCode": ["12345","686838"],
        "startTime": "2021-04-16 13:30:00",
        "endTime": "2021-04-16 14:30:00"
}
}
```

**请求体示例6 --多个自定义对象传参,对象顺序按照dubbo接口定义的传参顺序(xxdtox、xxdto)**

```json
{
    "serviceName": "xxxx",
    "methodName": "xxxxxx",
    "data": {
        "dto1": {
            "userCode": "7932723",
            "startTime": "2021-04-16 13:30:00",
            "endTime": "2021-04-16 14:30:00"
        },
        "dto2": {
            "name": "fang",
            "age": "20"
        }
    }
}
```



**返回值示例（成功）只展示其中一种**

```json
{
    "responseData": "dubbo接口返回什么，就返回什么"
}

```

**返回值示例（失败）**

```json
{
    "responseCode": 400,
    "responseMsg": "相应的异常信息"
}
```

 ### 3）查询服务名的配置信息

**接口地址**

- 说明：根据dubbo接口服务名，查询服务名下的配置信息(url,端口,dubbo版本,服务版本等)
- 地址：`/api/dubbo/search`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                               |
| ---- | ----------- | ------ | ---------------------------------- |
| 1    | serviceName | String | 服务名                             |
| 2    | version     | String | 非必传，传值时查询指定版本号的服务 |

**请求体示例**

```json
{
  "serviceName": "string"
}
```

**返回体**

| 序号 | 键值         | 类型   | 说明                        |
| ---- | ------------ | ------ | :-------------------------- |
| 1    | responseCode | Int    | 返回code                    |
| 2    | responseMsg  | String | 返回信息                    |
| 3    | responseData | Array  | data数组                    |
| 4    | - xx         | String | 省略,具体可问开发相关的解释 |

**返回值示例（成功）**

```json
{
  "responseCode": 200,
  "responseMsg": "请求成功",
  "responseData": {
    "url": "xxxx",
    "dubbo_service": "xxxx",
    "anyhost": "xxxx",
    "application": "xxxx",
    "bean.name": "xxxxx",
    "dubbo": "xxxx",
    "generic": "xxxx",
    "interface": "xxxx",
    "methods": [
      "xxxx",
      "xxxx",
      "xxxx"
    ],
    "owner": "xxxx",
    "pid": "xxxx",
    "revision": "xxxx",
    "side": "xxxx",
    "timeout": "xxxx",
    "timestamp": "xxxx"
  }
}

```

**返回值示例（失败）**

```json
{
    "responseCode": 400,
    "responseMsg": "相应的异常信息"
}
```

 ### 4）通过ip+端口查询服务名下的所有方法

**接口地址**

- 说明：根据dubbo接口地址和dubbo接口服务名，查询服务名下的所有方法
- 地址：`/api/dubbo/telnet/list`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                                                 |
| ---- | ----------- | ------ | ---------------------------------------------------- |
| 1    | serviceName | String | 服务名                                               |
| 2    | methodName  | String | 非必传，查询服务名下指定方法名的传值类型，不传查所有 |
| 3    | url | String | ip+端口，格式为"192.168.242.72:30912"                                               |

**请求体示例**

```json
{
   "url": "192.168.242.72:30912",
  "serviceName": "string",
  "methodName": "string"
}
```

**返回体**

| 序号 | 键值         | 类型   | 说明         |
| ---- | ------------ | ------ | :----------- |
| 1    | responseCode | Int    | 返回code     |
| 2    | responseMsg  | String | 返回信息     |
| 3    | responseData | Array  | data数组     |
| 4    | - param_type  | Array  | 方法传值类型 |
|      | - method | String | 方法名       |

**返回值示例（成功）**

```json
{
  "responseCode": 0,
  "responseMsg": "请求成功",
  "responseData": [
    {
      "method": "queryProductStoreInfo",
      "param_type": [
        "cn.com.xxxx.mallerp.dto.store.ProductStoreQueryRequest"
      ]
    }
  ]
}
```

**返回值示例（失败）**

```json
{
    "responseCode": 400,
    "responseMsg": "相应的异常信息"
}
```