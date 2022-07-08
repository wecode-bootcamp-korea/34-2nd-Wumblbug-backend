import json, jwt

from django.test import TestCase, Client
from django.conf import settings

from .models        import User

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
            id         = 1,
            kakao_id   = 112343434,
            email      = 'test@mail.com',
            nickname   = "test"
        )
        self.token = jwt.encode({'user_id' :User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()

    def test_success_user_view_get(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        token    = header['HTTP_Authorization']

        payload  = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user     = User.objects.get(id = payload['user_id'])

        response = client.get("/users", **header, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': response.json()['result']})
