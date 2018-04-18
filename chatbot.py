import sys
import json
import random
import logging
import requests
from functools import reduce
import config

#########################################################
logger = logging.getLogger('wechat')

#########################################################
class ChatBot:
    def __init__(self, agent = config.AGENT):
        self.url = config.CHATBOT_URL
        self.agent = agent

    def replay_in_sleepping(self):
        replies = ['维护中，很快就好...', '过会再聊吧，我需要休息一下子...', '[困]困死了，待会再聊吧...', '[哈欠]...zzzZZZ']
        return [{'type':'text', 'content': self._get_one_of(replies)}]

    def reply_to_unknown(self):
        replies = ['声音有点小，没听清呢☹️', '不好意思，刚没听清，麻烦您再说一遍？']
        return [{'type':'text', 'content': self._get_one_of(replies)}]

    def reply_to_text(self, user_id, query): 
        request_json = { "query": { "query": query, "confidence":1.0 }, 
                         "session": user_id, 
                         "agent": self.agent
                       } 
        return self._get_reply(request_json)      

    def reply_to_media(self, user_id, picture_id, url, media_id):
        if picture_id:
            request_json = self._get_recognized_pic_event(user_id, picture_id)
        else:
            request_json = self._get_unknown_pic_event(user_id, url, media_id)
        return self._get_reply(request_json)
    
    def reply_to_order_pay(self, user_id, orderId):
        request_json = { "event": { "name"     : "user-order-pay",
                                    "content" : { "order-id": orderId}},
                         "session" : user_id, 
                         "agent": self.agent
                       }
        return self._get_reply(request_json)

    def reply_to_subscribe(self, user_id):
        return self._get_reply(self._get_subscribe_event(user_id))

    def _get_subscribe_event(self, user_id):
        request_json = { "event": { "name" : "user-subscribe"},
                         "session": user_id, 
                         "agent": self.agent
                       }
        return request_json

    def _get_recognized_pic_event(self, user_id, picture_id):
        request_json = { "event": { "name" : "identify-product",
                         "content" : {"product-id": picture_id}}, 
                         "session":user_id, 
                         "agent": self.agent
                       }
        return request_json                       

    def _get_unknown_pic_event(self, user_id, url, media_id):
        request_json = { "event": { "name" : "unknown-product",
                                    "content" : {"image-url": url, "media_id": media_id}}, 
                          "session":user_id, 
                          "agent": self.agent
                       }
        return request_json

    def _get_reply(self, request_json):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url=self.url, headers=headers, data=json.dumps(request_json))
            if response.status_code != 200: 
                logger.error('requested chatbot failed, error code = {0}!'.format(response.status_code))
                return self.replay_in_sleepping()
            return self._generate_reply(response.json())
        except Exception as e:
            logger.error('requested chatbot exception: {0}!'.format(str(e)))
            return self.replay_in_sleepping()

    def _generate_reply(self, chatbot_reply):
        logger.info('received from chatbot: {0}'.format(chatbot_reply))
        text_replies = chatbot_reply['reply'] if 'reply' in chatbot_reply else []
        media_replies  = chatbot_reply['data'] if 'data' in chatbot_reply else []

        replies = []
        for text_reply in text_replies:
            replies.append({'type' : 'text', 'content' : text_reply})
        for media_reply in media_replies:
            if 'type' not in media_reply:
                logger.error('chatbot reply data without type')
                continue
            if media_reply['type'] == 'image':
                replies.append({'type': 'image', 'content' : media_reply})
            elif media_reply['type'] == 'article':
                replies.append({'type': 'article', 'content': media_reply})
            elif media_reply['type'] == 'qrcode':
                replies.append({'type': 'qrcode', 'content' : media_reply})
            elif media_reply['type'] == 'custom-service':
                replies.append({'type': 'custom-service', 'content' : media_reply})
            else:
                logger.error('chatbot reply unkown message type : {0}'.format(media_reply['type']))
        return replies

    def _get_one_of(self, array):
        return array[random.randint(0, len(array)-1)]        