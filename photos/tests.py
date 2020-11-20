from django.test.utils import setup_test_environment
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from account.models import Account
from photos.models import Image

# Create your tests here.

def create_account():
    return Account.objects.create(username="Jamie", first_name="James", last_name="Bond", email="j@b.com", id=2)

def get_token():
    return Token.objects.get(user_id=2)

def add_photos():
    return Image.objects.create(username="Jamie", thumbnail=b'ABCD')

def get_photos():
    return Image.objects.get(username="Jamie")

class PhotoAPITests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        create_account()
        add_photos()
        

    def test_getting_photos_with_username(self):
        res = get_token()
        response = self.client.get("/photos/get", {"username": "Jamie"}, **{"HTTP_AUTHORIZATION" : "Token " + str(res)})
        self.assertNotEqual(len(response.data), 0, "Did not return data successfully")

    def test_getting_photos_with_invalid_username(self):
        res = get_token()
        response = self.client.get("/photos/get", {"username": "Invalid"}, **{"HTTP_AUTHORIZATION" : "Token " + str(res)})
        self.assertEqual(len(response.data), 0)

    def test_getting_photos_with_no_username(self):
        res = get_token()
        response = self.client.get("/photos/get", **{"HTTP_AUTHORIZATION" :  "Token " + str(res)})
        self.assertEqual(response.data["message"], "Images could not be fetched.")

    def test_full_screen_image_fetching(self):
        res = get_token()
        response = self.client.get("/photos/getImage", {"id": "1"}, **{"HTTP_AUTHORIZATION" :  "Token " + str(res)})
        self.assertEqual(response.data["id"], 1)

    def test_non_existing_image_fetching(self):
        res = get_token()
        response = self.client.get("/photos/getImage", {"id": "-1"}, **{"HTTP_AUTHORIZATION" :  "Token " + str(res)})
        self.assertEqual(response.data["message"], "Full screen image could not be fetched")

    def test_image_fetching_with_invalid_id(self):
        res = get_token()
        response = self.client.get("/photos/getImage", {"id": "A"}, **{"HTTP_AUTHORIZATION" :  "Token " + str(res)})
        self.assertEqual(response.data["message"], "Full screen image could not be fetched")
