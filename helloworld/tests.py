from django.test import TestCase, RequestFactory
from helloworld.views import HomePageView
from unittest import mock
import slack
import slackbot_settings
import slackbot.dispatcher
import plugins.hello
from helloworld.models import Response
from helloworld.models import Sorry

class HelloWorldTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.greeting = Response.objects.create(question="おはよう", answer="おはようございます")
        self.sorry = Sorry.objects.create(answer="え！")

    def test_home_page(self):
        request = self.factory.get('/')
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/html; charset=utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Congratulations')

    def test_post_return_no_user(self):
        data = {}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no user')

    def test_post_return_unauthorized_user(self):
        data = {"user_id": "123"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'unauthorized user')

    def test_post_return_no_parameter(self):
        data = {"user_id": "UB9AVTDT3", "channel_name": "prj-slackapp"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no parameter')

    def test_post_return_invalid_parameter(self):
        data = {"user_id": "UB9AVTDT3", "channel_name": "prj-slackapp", "text": "#prj-slackapp-test"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid parameter')

    def test_post_return_no_message(self):
        data = {"user_id": "UB9AVTDT3", "channel_name": "prj-slackapp", "text": '#prj-slackapp-test ""'}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no message')

    def test_post_return_invalid_channel(self):
        data = {"user_id": "UB9AVTDT3", "channel_name": "prj-slackapp", "text": '#abc "test"'}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid channel')

    def test_post_call_chat_postMessage(self):
        client = slack.WebClient(token=slackbot_settings.API_TOKEN)
        slack.WebClient = mock.MagicMock(return_value=client)
        client.chat_postMessage = mock.MagicMock()

        data = {"user_id": "UB9AVTDT3", "channel_name": "prj-slackapp", "text": '#prj-slackapp-test "test"'}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        client.chat_postMessage.assert_called_with(channel="CHXS0FH5M",text="test",as_user=True)

    def test_mention_func_greeting(self):
        body = {'text': 'おはよう', 'user': 'UB9AVTDT3'}
        excepted = 'おはようございます'
        self.assert_called_massage_reply(body, excepted)

    def test_mention_func_sorry(self):
        body = {'text': 'こんにちは', 'user': 'UB9AVTDT3'}
        excepted = 'え！'
        self.assert_called_massage_reply(body, excepted)

    def assert_called_massage_reply(self, body, excepted):
        message = slackbot.dispatcher.Message(None, body)
        message.reply = mock.MagicMock()
        plugins.hello.mention_func(message)

        message.reply.assert_called_with(excepted)
