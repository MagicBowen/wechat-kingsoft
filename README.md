# Wechat for Chatbot

- Setup a python file named `config.py` in the root path of this project;
- Add follow varable definations and modify each value to yours;

```python
TOCKEN = 'test'
APP_ID = 'wxf164ebf08b919a0f'
APP_SECRET = 'ddb3252ecbcb79f47a44f1a049013546'
ENCRYPT = True
ENCODING_AES_KEY ='KD4kyN1crLqOaRf8QpkfOTHhd2lscisWBZAiAhf4IbY'
CHATBOT_URL = 'http://127.0.0.1:8080/query'
AGENT_NAME = 'kingsoft-demo'
```
If `ENCRYPT = False`, `ENCODING_AES_KEY` is not needed.

- Run project by : `python3 run.py`;