from django.test import TestCase, RequestFactory
from helloworld.views import HomePageView
from unittest import mock
import slack
import slackbot_settings

class HelloWorldTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

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
        data = {"user_id": "UB9AVTDT3"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no parameter')

    def test_post_return_invalid_parameter(self):
        data = {"user_id": "UB9AVTDT3", "text": "prj-slackapp-test"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid parameter')

    def test_post_return_no_message(self):
        data = {"user_id": "UB9AVTDT3", "text": "prj-slackapp-test,"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no message')

    def test_post_return_invalid_channel(self):
        data = {"user_id": "UB9AVTDT3", "text": "abc,test"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid channel')

    def test_post_call_chat_postMessage(self):
        client = slack.WebClient(token=slackbot_settings.API_TOKEN)
        slack.WebClient = mock.MagicMock(return_value=client)
        client.chat_postMessage = mock.MagicMock()

        data = {"user_id": "UB9AVTDT3", "text": "prj-slackapp-test,test"}
        request = self.factory.post('/', data)
        response = HomePageView.as_view()(request)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        client.chat_postMessage.assert_called_with(channel="CHXS0FH5M",text="test",as_user=True)
