import email
from email.quoprimime import body_check
import json, jwt
from urllib import response
from wsgiref import headers

from django.test import TestCase, Client
from django.conf import settings

from .models        import User
from unittest.mock  import patch, MagicMock

class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao_id   = 2329972136,
            email      = "chaduri7913@naver.com",
            nickname   = "조현우"
        )
        pass
    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_kakao_signinView_new_user(self, mocked_requests):
        client   = Client()

        class MockedResponse:
            def json(self):
                return {
                        "id" : 2329972136,
                        "kakao_account" : {
                            "email" : "chaduri7913@naver.com"
                        },
                        "properties" :{
                            "nickname" : "조현우"
                        }
                    }
                
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        # headers             = {"HTTP_Authorization" : "asdfsc123asd.asdf123dacvsdfg"}
        body                = {"code" : "asdf112"}
        response            = client.post("/signin/kakao", data=body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'token': response.json()['token']})

                
    @patch("users.views.requests")
    def test_fail_kakao_signinView_post_invalid_keys(self, mocked_requests):
        client   = Client()

        class MockedResponse:
            def json(self):
                return {
                        "id" : 2329972136,
                        "kakao_account" : {
                            "email" : "chaduri7913@naver.com"
                        },
                        "properties" :{
                            "nickname" : "조현우"
                        }
                    }
                
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        # headers             = {"HTTP_Authorization" : "asdfsc123asd.asdf123dacvsdfg"}
        body                = {"code1" : "asdf112"}
        response            = client.post("/signin/kakao", data=body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'token': response.json()['token']})

