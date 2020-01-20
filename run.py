# coding: utf-8

from slackbot.bot import Bot
import django
import os

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ec2django.settings")
    django.setup()
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('start slackbot')
    main()

