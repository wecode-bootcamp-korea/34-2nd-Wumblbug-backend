import json
from datetime import date

import jwt
from django.test import TestCase, Client
from django.conf import settings

from .models        import User, Like
from projects.models import Category, Project
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
    def test_success_kakao_signinView_login(self, mocked_kakao):
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

    @patch("users.views.KakaoAPI")
    def test_success_kakao_signinView_signup(self, mocked_kakao):
        client   = Client()

        class MockedResponse:
            def get_kakao_token(self, code):
                return 'kakao_token'
            
            def get_kakao_profile(self, access_token):
                return {
                        "id" : 11223345,
                        "kakao_account" : {
                            "email"                 : "ytuhjk@naver.com",
                            'has_email'             : True,
                            'email_needs_agreement' : False, 
                            'is_email_valid'        : True, 
                            'is_email_verified'     : True, 

                        },
                        "properties" :{
                            "nickname" : "test2"
                        }
                    }

        mocked_kakao.return_value = MockedResponse()
        
        body     = {"code" : "asdf122312"}
        response = client.post("/users/signin/kakao", json.dumps(body), content_type = 'application/json')
        
        access_token = jwt.encode({'user_id' : 2}, settings.SECRET_KEY, settings.ALGORITHM)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'token' : access_token})

    @patch("users.views.KakaoAPI")
    def test_keyerror_kakao_signinView_login(self, mocked_kakao):
        client   = Client()

        class MockedResponse:
            def get_kakao_token(self, code):
                return 'kakao_token'
            
            def get_kakao_profile(self, access_token):
                return {
                        "id" : 11223345,
                        "kakao_account" : {
                            "email"                 : "ytuhjk@naver.com",
                            'has_email'             : True,
                            'email_needs_agreement' : False, 
                            'is_email_valid'        : True, 
                            'is_email_verified'     : True, 

                        },
                        "properties" :{
                            "nickname" : "test2"
                        }
                    }

        mocked_kakao.return_value = MockedResponse()
        
        body     = {"code1" : "asdf122312"}
        response = client.post("/users/signin/kakao", json.dumps(body), content_type = 'application/json')
        
        access_token = jwt.encode({'user_id' : 2}, settings.SECRET_KEY, settings.ALGORITHM)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'KEY_ERROR'})

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

class LikeTest(TestCase):
    def setUp(self):
        User.objects.create(
            id         = 1,
            kakao_id   = 112343434,
            email      = 'test@mail.com',
            nickname   = "test"
        )

        Category.objects.create(
            id        = 1,
            name      = "쥬얼리",
            image_url = "ss" 
        )

        Project.objects.create(
            id              = 1,
            user            = User.objects.get(id=1),
            category        = Category.objects.get(id=1),
            title           = "에메랄드 링",
            shortcut_title  = "에메랄드 링",
            summary         = "에메랄드 링",
            total_amount    = 0,
            price           = 20000,
            thumbnail       = "sss",
            pk_uri          = "emerald_ring",
            target_amount   = 5000000,
            start_datetime  = "2022-07-09",
            end_datetime    = "2022-08-01",
            pay_end_date    = "2022-08-02",
            settlement_date = "2022-08-03",
            introduction    = "예쁜 링",
            budget_plan     = "없음"
        )

        self.token = jwt.encode({'user_id' :User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Project.objects.all().delete()

    def test_success_like_view_post(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}

        body       = {"project_id" : 1}
        response = client.post("/users/like", **header, content_type='application/json', data=json.dumps(body))
        project    = Project.objects.get(id=body['project_id'])
        like_count = Like.objects.filter(project=project).count()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS', 'LIKE_COUNT': like_count})

    def test_keyerror_like_view_post(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}

        body     = {"project_id1" : 1}
        response = client.post("/users/like", **header, content_type='application/json', data=json.dumps(body))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "KEY_ERROR"})

    def test_success_like_view_get(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        token    = header['HTTP_Authorization']

        payload    = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id    = payload['user_id']
        response   = client.get("/users/like", **header, content_type='application/json')

        like_projects = Like.objects.filter(user=User.objects.get(id=1))
        today         = date.today()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"RESULT" : [
            {
                "user_id"       : user_id,
                "project_id"    : 1,
                "thumbnail"     : "sss",
                "category"      : 1,
                "title"         : "에메랄드 링",
                "summary"       : "에메랄드 링",
                "total_amount"  : 0,
                "remain_days"   : (like_project.project.end_datetime - today).days
            } for like_project in like_projects
        ]}
)