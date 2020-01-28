# helloworld/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import slack
import slackbot_settings
import re


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    def post(self, request):
      rs = ""
      if "user_id" in request.POST:
          user_id = request.POST["user_id"]
          client = slack.WebClient(token=slackbot_settings.API_TOKEN)
          prj_channel = client.channels_info(channel="CBU2YJSGM")
          if prj_channel["channel"]["members"].count(user_id) > 0:
              if "text" in request.POST:
                  params = re.match(r'#(\S+)\s"(.*?)(?<!\\)"', request.POST["text"])
                  if params is not None:
                      if len(params.group(2)) > 0:
                          channels = client.channels_list()
                          send_channel = ""
                          if params.group(1) != request.POST["channel_name"]:
                              for channel in channels['channels']:
                                  if params.group(1) == channel['name']:
                                      send_channel = channel['id']
                                      break
                          if send_channel:
                              client.chat_postMessage(channel=send_channel, text=params.group(2), as_user=True)
                              rs = params.group(2)
                          else:
                              rs = "invalid channel"
                      else:
                          rs = "no message"
                  else:
                      rs = "invalid parameter"
              else:
                  rs = "no parameter"
          else:
              rs = "unauthorized user"
      else:
          rs = "no user"
      return HttpResponse(rs, content_type="text/plain")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(HomePageView, self).dispatch(*args, **kwargs)