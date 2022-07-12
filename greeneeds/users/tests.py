import json

import jwt
from django.test import TestCase, Client
from django.conf import settings

from .models        import User
from unittest.mock  import patch, MagicMock

class test_KakaoSignin(TestCase):
    def setUp(self):
        User.objects.create(
            id         = 1,
            kakao_id   = 11223344,
            email      = "asdfqwer@naver.com",
            nickname   = "test"
        )
    
    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.KakaoAPI")
    def test_success_kakao_signinView_new_user(self, mocked_kakao):
        client   = Client()

        class MockedResponse:
            def get_kakao_token(self, code):
                return 'kakao_token'
            
            def get_kakao_profile(self, access_token):
                return {
                        "id" : 11223344,
                        "kakao_account" : {
                            "email"                 : "asdfqwer@naver.com",
                            'has_email'             : True,
                            'email_needs_agreement' : False, 
                            'is_email_valid'        : True, 
                            'is_email_verified'     : True, 

                        },
                        "properties" :{
                            "nickname" : "test"
                        }
                    }

        mocked_kakao.return_value = MockedResponse()
        
        body     = {"code" : "asdf112"}
        response = client.post("/users/signin/kakao", json.dumps(body), content_type = 'application/json')
        
        access_token = jwt.encode({'user_id' : 1}, settings.SECRET_KEY, settings.ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'token' : access_token})
                
    # @patch("users.views.requests")
    # def test_fail_kakao_signinView_post_invalid_keys(self, mocked_requests):
    #     client   = Client()

    #     class MockedResponse:
    #         def json(self):
    #             return {
    #                     "id" : 11223344,
    #                     "kakao_account" : {
    #                         "email"                 : "asdfqwer@naver.com",
    #                         'has_email'             : True,
    #                         'email_needs_agreement' : False, 
    #                         'is_email_valid'        : True, 
    #                         'is_email_verified'     : True, 

    #                     },
    #                     "properties" :{
    #                         "nickname" : "test"
    #                     }
    #                 }
                
    #     mocked_requests.get = MagicMock(return_value = MockedResponse())
    #     # headers             = {"HTTP_Authorization" : "asdfsc123asd.asdf123dacvsdfg"}
    #     body                = {"code1" : "asdf112"}
    #     response            = client.post("users/signin/kakao", json.dumps(body), content_type = 'application/json')

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), {'MESSAGE': 'KEY_ERROR})

