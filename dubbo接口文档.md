# 基于http协议dubbo接口文档

> 原理：基于python  telnetlib库，模拟Telnet命令进行dubbo接口测试，再封装成http接口
>
> 备注：部署的服务，必须可以连接上dubbo服务主机

## 前言

### 修改记录

| 编号 | 修改日期 | 修改内容 | 修改人 |
| ---- | -------- | -------- | ------ |
| 1    | 2021-3-9 | 创建文档 | Fang   |
|      |          |          |        |
|      |          |          |        |

### 服务地址

测试环境：http://xxx.xx.xx.xx:32767

 ## 接口说明

 ### 1）查询服务名下的所有方法

**接口地址**

- 说明：根据dubbo接口地址和dubbo接口服务名，查询服务名下的所有方法
- 地址：`/api/dubboList`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                   |
| ---- | ----------- | ------ | ---------------------- |
| 1    | url         | String | dubbo接口地址，IP:端口 |
| 2    | serviceName | String | 对应的服务名           |
| 3    | methodName  | String | 服务名下对应的方法名   |

**请求体示例**

```json
{
    "url": "xxx.xxx.xx.xx:20880",
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx"
}
```

**返回体**

| 序号 | 键值         | 类型   | 说明                                                |
| ---- | ------------ | ------ | :-------------------------------------------------- |
| 1    | responseCode | Int    | 返回code                                            |
| 2    | responseMsg  | String | 返回信息                                            |
| 3    | responseData | Array  | data数组                                            |
| 4    | - type       | int    | 0-枚举值，1-无需传参<br />2- 集合对象，3-自定义对象 |
|      | - paramType  | string | Java传值类型                                        |
|      | - methodName | string | 方法名                                              |

**返回值示例（成功）**

```json
{
    "responseCode": 200,
    "responseMsg": "请求成功",
    "responseData": [
        {
            "methodName": "xxxxxx",
            "paramType": "java.util.HashMap",
            "type": 3
        },
        {
            "methodName": "xxxxxx",
            "paramType": [
                "java.lang.String",
                "java.lang.String",
                "java.lang.String",
                "java.lang.Integer",
                "java.lang.Integer"
            ],
            "type": 0
        },
        {
            "methodName": "xxxxxx",
            "paramType": "",
            "type": 1
        },
        {
            "methodName": "xxxxxx",
            "paramType": "java.util.List",
            "type": 2
        }
    ]
}
```


**返回值示例（失败）**

```json
{
    "responseCode": 500,
    "responseMsg": "相应的报错信息"
}
```



### 2）dubbo接口-业务接口

**接口地址**

- 说明：根据dubbo接口地址和dubbo接口服务名，方法名，参数值实现dubbo接口逻辑
- 地址：`/api/dubbo`
- 方法：`POST`

**请求头**

| 序号 | 类型         | 值               | 说明      |
| ---- | ------------ | ---------------- | --------- |
| 1    | Content-Type | application/json | JSON 格式 |

**请求体**

| 序号 | 键值        | 类型   | 说明                    |
| ---- | ----------- | ------ | ----------------------- |
| 1    | url         | string | dubbo接口地址，IP:端口  |
| 2    | serviceName | string | 服务名                  |
| 3    | methodName  | string | 方法名                  |
| 4    | data        | object | 传值4种情况，具体看示例 |

**请求体示例 -- 原生对象或者自定义对象传参**

```json
{
    "url": "xxx.xxx.xx.xx:20880",
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx",
    "methodName": "xxxxxx",
    "data": {        //data传入对应的业务json数据
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
```
**请求体示例 -- 枚举值类型传参**

```json
{
    "url": "xxx.xxx.xx.xx:20880",
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx",
    "methodName": "login",
    "data": {         //格式为json，顺序必须按照dubbo接口枚举值传参顺序，注意是否为int还是string
        "account":"80563855",
        "password":"3fd6ebe43dab8b6ce6d033a5da6e6ac5"
    }
}
```

**请求体示例 -- 方法名无需传参**

```json
{
    "url": "xxx.xxx.xx.xx:20880",
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx",
    "methodName": "xxxxxx",
    "data":{}      //传入空对象
}
```

**请求体示例 --集合对象传参**

```json
{
    "url": "xxx.xxx.xx.xx:20880",
    "serviceName": "cn.com.xxx.mallerp.api.xxxx.xxxx",
    "methodName": "xxxxxx",
    "data":{
        "empList": [
            "30000445",
            "30000444"
        ]
    } //传入对象，里面嵌套数组
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
    "responseCode": 500,
    "responseMsg": "相应的报错信息"
}
```

