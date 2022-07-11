import email
import json
from urllib import response
from wsgiref import headers

from django.test import TestCase, Client

from .models     import User
from unittest    import patch, MagicMock

class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao_id   = 2329972136,
            email      = "chaduri7913@naver.com",
            nickname   = "조현우"
        )
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
        headers             = {"Authorization" : "asdfsc123asd.asdf123dacvsdfg"}
        response            = client.get("/signin/kakao", **headers)

        self.assertEqual(response.status_code, 201)
                
    @patch("users.views.requests")
    def test_fail_KakaoSigninView_post_invalid_keys(self, mocked_requests):
        client = Client()

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
        headers             = {"Authorization" : "asdfsc123asd.asdf123dacvsdfg"}
        response            = client.get("/signin/kakao", **headers)

        self.assertEqual(response.status_code, 201)