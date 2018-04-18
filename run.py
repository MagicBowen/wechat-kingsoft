import os
import sys
sys.path.append("lib/itchat")
import itchatmp
import json
# import qrcode
import time
import logging
import time
import requests
import config
from chatbot import ChatBot
from register_menu import register_menu
from user_id import UserId

#########################################################
logger = logging.getLogger('wechat')

USER = UserId()
#########################################################
# for production environment
#########################################################
itchatmp.update_config(itchatmp.WechatConfig(
    token = config.TOCKEN,
    appId = config.APP_ID,
    appSecret = config.APP_SECRET,
    encryptMode = itchatmp.content.SAFE if config.ENCRYPT else itchatmp.content.NORMAL,
    encodingAesKey = config.ENCODING_AES_KEY if config.ENCRYPT else ''))

#########################################################
def get_image_name_from_url(tag, url):
    fileName = url.split('=')[-1]
    return fileName

def fetch_image(tag, url):
    result = requests.get(url)
    if result.status_code != 200: 
        logger.error('fetch image {} failed!'.format(url))
        return None
    file_name = get_image_name_from_url(tag, url)
    if not os.path.exists('./uploads'): os.makedirs('./uploads')
    file_path = 'uploads/{}'.format(file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as file:
            file.write(result.content)
    return file_path

def download_media(media_id):
    r = itchatmp.messages.download(media_id)
    if 'File' in r:
        if not os.path.exists('./downloads'): os.makedirs('./downloads')
        file_path = os.path.join('./downloads', r.get('FileName', 'unknown.jpg'))
        with open(file_path, 'wb') as f:
            f.write(r['File'].getvalue())
        return file_path

# def get_picture_id(media_id):
#     file = download_media(media_id)
#     if not file: return None
#     return qrcode.scan(file)      

#########################################################
def construct_reply(reply, user_id, active = False):
    content = reply['content']
    if reply['type'] == 'article':
        print('Reply article')
        title = content['title']
        description = content['description']
        picture_url = content['cover-url']
        article_url = content['content-url']
        article = {'Title':title,'Description':description,'PicUrl':picture_url,'Url':article_url}
        if active : article = {'title':title,'description':description,'picurl':picture_url,'url':article_url}
        return {'MsgType' : itchatmp.content.NEWS,
                'Articles' : [article]}
    elif reply['type'] == 'image':
        print('Reply image')
        pic_tag = content['tag']
        pic_url = content['url']
        logger.error("content is "+ str(content))
        if ('payment' in content) and (content['payment'] == 'wx'):
            itchatmp.send("请您使用微信扫描下面二维码支付，谢谢", user_id)
            return generate_qr_code_url(user_id)
        image = fetch_image(pic_tag, pic_url)
        print('image = ' + image)
        if not image: raise Exception('fetch image from {} failed'.format(pic_url))
        return {'MsgType': itchatmp.content.IMAGE,'FileDir': image}
    elif reply['type'] == 'qrcode':
        print('Reply qrcode')
        orderId = content['orderId']
        return generate_qr_code_url(orderId)
    elif reply['type'] == 'custom-service':
        print('Reply custom-service')
        return generate_reply_by_custom_service(user_id)
    print('Reply text')
    return content

#########################################################
def active_reply(replies, user_id):
    for reply in replies:
        try:
            itchatmp.send(construct_reply(reply, user_id, True), user_id)
        except Exception as e:
            print('Exception occured when active send!')   

#########################################################
def reply_to_user(replies, user_id = None):
    if len(replies) > 1:
        active_reply(replies[0:-1], user_id)
    return construct_reply(replies[-1], user_id)

########################################################
@itchatmp.access_token
def get_access_token(accessToken=None):
    return accessToken

def generate_reply_by_custom_service(user_id):
    if (has_online_customer()):
        itchatmp.send("正在帮您接通人工客服，请稍等...", user_id)
        return {'MsgType' : itchatmp.content.TRANSFER}
    return "抱歉，当前客服座席忙，稍后会主动联系您..."

def has_online_customer():
    customUrl = "https://api.weixin.qq.com/cgi-bin/customservice/getonlinekflist?access_token=" + get_access_token()
    logger.error("customUrl is:" + customUrl)
    online_customer = json.loads(requests.get(customUrl).text)
    logger.error("online customer is " + str(online_customer))
    if (len(online_customer["kf_online_list"]) < 1) :
        return False
    else:
        return True

def generate_qr_code_url(orderId):
    wxUrl = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=" + get_access_token()
    logger.error("qr generate url is:" + wxUrl)
    body = {"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": orderId}}}
    rsp = requests.post(wxUrl, json=body)
    picture_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+  json.loads(rsp.text)['ticket']
    imagePath = fetch_image("qrCode", picture_url)
    logger.error("local file path:" + imagePath)
    if not imagePath: raise Exception('fetch image from {} failed'.format(picture_url))
    return {'MsgType': itchatmp.content.IMAGE,'FileDir': imagePath}
    
#########################################################
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    user_id = msg['FromUserName']
    content = msg['Content']
    print("receive text")
    return reply_to_user(ChatBot(USER.get_role(user_id)).reply_to_text(user_id, content), user_id)

#########################################################
@itchatmp.msg_register(itchatmp.content.VOICE)
def voice_reply(msg):
    user_id = msg['FromUserName']
    content = msg['Recognition']
    chatbot = ChatBot(USER.get_role(user_id))
    print("receive voice")
    if not content or content.strip() == '': return reply_to_user(chatbot.reply_to_unknown(user_id))
    return reply_to_user(chatbot.reply_to_text(user_id, content), user_id)


#########################################################
@itchatmp.msg_register(itchatmp.content.EVENT)
def subscribe_reply(msg):
    user_id = msg['FromUserName']
    if msg['Event'] == 'subscribe' :
        print("receive event: subscribe")
        return reply_to_user(ChatBot(USER.get_role(user_id)).reply_to_subscribe(user_id), user_id)
    elif msg['Event'] == 'SCAN' :
        print("receive event: SCAN")
        return reply_to_user(ChatBot(USER.get_role(user_id)).reply_to_order_pay(user_id, msg['EventKey']), user_id)
    elif msg['Event'] == 'CLICK' :
        print("receive event: CLICK")
        role_id = msg['EventKey']
        USER.set_role(user_id, role_id)
        return USER.role_modified_reply(role_id)
    return ''

#########################################################
# @itchatmp.msg_register(itchatmp.content.IMAGE)
# def image_reply(msg):
#     user_id = msg['FromUserName']
#     media_id = msg['MediaId']
#     image_url = msg['PicUrl']
#     picture_id = get_picture_id(media_id)
#     return reply_to_user(ChatBot(USER.get_role(user_id)).reply_to_media(user_id, picture_id, image_url, media_id), user_id)
 
#########################################################
register_menu()
itchatmp.run(port=config.HTTP_PORT)    
