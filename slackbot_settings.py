# coding: utf-8
import boto3
import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('CHIEMI_SLACKAPP_BOT_TOKEN')
if API_TOKEN is None:
    ssm = boto3.client('ssm', region_name='ap-northeast-1')
    parameter = ssm.get_parameter(Name='chiemi_slackapp_bot_token', WithDecryption=True)
    API_TOKEN = parameter['Parameter']['Value']

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "Sorry but I didn't understand you"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']