
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from shortcut.settings import PATH_URL_SHORT, URL_API
from shorturl.models import User, Url
from shorturl.views import get_short_code


class UserTestCase(TestCase):

    def test_create_user(self):

        user = User(name="chaordic")
        user.save()

        self.assertEqual(User.objects.count(), 1)

    def test_update_user(self):

        user = User(name="chaordic")
        user.save()

        user.name = "change name"
        user.save()

        self.assertEqual(User.objects.filter(name__exact="change name").count(), 1)

    def test_delete_user(self):

        user = User(name="chaordic")
        user.save()

        User.objects.get(pk=user.pk).delete()

        self.assertEqual(User.objects.all().count(), 0)

    def test_create_url(self):

        user = User(name='chaordic')
        user.save()

        url = Url(url="https://www.chaordic.com.br", shortUrl="http://127.0.0.1/" + PATH_URL_SHORT + get_short_code())
        url.user = user
        url.save()

        self.assertEqual(Url.objects.all().count(), 1)


class TestAPI(APITestCase):

    def test_create_user_201(self):

        data = {
            'id': 'chaordic'
        }

        response = self.client.post(URL_API + 'user/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)