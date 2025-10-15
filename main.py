from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FlexSendMessage,ImageSendMessage

import configparser
import json
import grab
import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'
worknum=0
url1=""
url2=""
# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    global worknum,url1,url2
    message = event.message.text
    if worknum==100:
        worknum=0
        url1,url2 = grab.run_stock(str(message))
        reply_arr=[]
        reply_arr.append(ImageSendMessage(
                original_content_url=url1,
                preview_image_url=url1
                ))
        reply_arr.append( ImageSendMessage(
                original_content_url=url2,
                preview_image_url=url2
                ))
        line_bot_api.reply_message(
            event.reply_token,reply_arr
        )
        
    if worknum==200:
        worknum=0
        text=grab.search_stockNO(str(message))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text)
        )
        
    if worknum==300:
        worknum=0
        text=grab.compare(str(message))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text)
        )
    
    if "開啟面板" in message:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('[使用選擇]',FindFlexMsg("selectFuction"))
        )
    if "查詢今日科技文章" in message:
        grab.run_article()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('[科技文章]',FindFlexMsg("articleLink"))
        )
    if "查詢今日股票交易" in message:
        worknum=100
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("請輸入股票代碼")
        )
    if "查詢公司股票代碼" in message:
        worknum=200
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("請輸入公司名稱")
        )

    if "查詢公司同業比較" in message:
        worknum=300
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("請輸入股票代碼")
        )

    if "查詢近期熱門話題" in message:
        worknum=0
        url = grab.search_hot_topic() 
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
                )
        )

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''
        
        for i in event.message.text:
        
            pretty_text += i
            pretty_text += random.choice(pretty_note)
    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )

def FindFlexMsg(file_name):
    FlexMessage = json.load(open("templates" + "//" + file_name + ".json",'r',encoding='utf-8'))
    return FlexMessage


if __name__ == "__main__":
    app.run()