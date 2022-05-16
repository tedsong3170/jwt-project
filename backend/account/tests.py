from django.test import TestCase, Client
from .models import User, UserManager
# Create your tests here.

class AccountTestCase(TestCase):
    def setUp(self) -> None:

        user = User.objects.create_user(
            email='song@song.com',
            nickname='song',
            password='song'
        )

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_login(self):
        c = Client()

        res = c.post(
            '/auth/login',
            {
                'email': 'song@song.com',
                'password': 'song'
            }
        )
        body = res.json()
        self.assertEqual(res.status_code, 200)