# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import re
from helloworld.models import Response
from helloworld.models import Sorry
import random
import slack
import slackbot_settings
import datetime
import sys

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@respond_to('.*')
def mention_func(message):
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    sys.stdout.write("%s,input,@%s,%s" % (datetime.datetime.now(tz_jst).strftime('%Y/%m/%d %H:%M:%S'), user_name(message.body['user']), message.body['text']))
    querySet = Response.objects.extra(where=["question glob %s"],params=[message.body['text']])
    obj = querySet.first()
    if obj is None:
        querySet = Sorry.objects.all()
        if querySet.count() > 0:
            obj = random.choice(querySet)
            message.reply(obj.answer) # メンション
            sys.stdout.write("%s,output,%s" % (datetime.datetime.now(tz_jst).strftime('%Y/%m/%d %H:%M:%S'), obj.answer))
    else:
        message.reply(obj.answer) # メンション
        sys.stdout.write("%s,output,%s" % (datetime.datetime.now(tz_jst).strftime('%Y/%m/%d %H:%M:%S'), obj.answer))

def user_name(user_id):
    client = slack.WebClient(token=slackbot_settings.API_TOKEN)
    users = client.users_list()
    names = [x['profile']['display_name'] for x in users['members'] if x['id'] == user_id]
    return names[0]