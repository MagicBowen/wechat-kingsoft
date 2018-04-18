# API

Robot会在指定的http endpoint上发布一个rest api。
和robot之间的每轮对话，需要构造对应格式的json消息，post到相应的http endpoint上，然后获得返回的json响应消息。

## request

post给robot的request消息分为`query`和`event`两类。
- `query` : 用户正常的对话请求；
- `event` : 客户端事件，例如用户登录，地理位置上报事件等等。需要提前和robot端约定事件意图、事件名和事件参数；

### query

```json
{ 
    "query"   : { "query": "Hello, XiaoDa!", "confidence":1.0 }, 
    "session" : "user-id", 
    "agent"   : "robot-name"
} 
```

- `query.query` : 用户的对话内容，为utf-8格式的字符串；
- `query.confidence` : 如果用户的对话内容是经过ASR处理后得到，该项为ASR的信心概率。浮点数，范围`0 ~ 1.0`。如果无法获得则默认填写`1.0`；
- `session` : 用户标识，用于区分不同user；
- `agent`   : 接收对话的robot的名字，用于区分不同的目标robot，需要提前约定；

### event

```json
{ 
    "event"   : { "name"     : "user-login",
                  "content"  : { "key1" : "value1", "key2" : "value2" }
                },
    "session" : "user-id", 
    "agent"   : "robot-name"
}
```

- `event.name`    : 事件名；
- `event.content` : 事件参数，自定义的json对象；
- `session` : 用户标识，区分不同user；
- `agent`   : 接收对话的robot的名字，用于区分不同的目标robot，需要提前约定；

## response

Robot返回的消息格式如下：

```json
{
    "intents": [ 
        {
            "name": "say-hi",
            "confidence": 1
        }
    ],
    "reply": [
        "Hi, welcome!"
    ]
}
```

- `intent` : 数组；用户的对话被识别的意图以及对应的信心概率指数，一般可以不用处理；
- `reply`  : 数组；robot返回给用户的对话，可以一次回复多句。如果展示端无法多句分开展示，则需要将所有内容合并成后展示给用户；

## code

以下是一段python示例代码；

```python
def query_robot(self, user_id, query, agent): 
    request_json = { 
                       "query"  : { "query": query, "confidence":1.0 }, 
                       "session": user_id, 
                       "agent"  : agent
                    } 

    headers = {'Content-Type': 'application/json'}
    # 假设robot发布的http endpoint为 “http://xiaoda.ai/kingsoft-demo/query”
    response = requests.post(url='http://xiaoda.ai/kingsoft-demo/query', headers=headers, data=json.dumps(request_json))
    if response.status_code != 200: 
        logger.error('Query robot failed, error code = {0}!'.format(response.status_code))
        return '请求robot发生错误，请您稍后再试...'
    return response.json['reply'][0]  # 假设robot返回单句
```