import json, jwt
from datetime import date

from django.test import TestCase, Client
from django.conf import settings

from .models          import User, Like
from projects.models  import Category, Project

class UserTest(TestCase):
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
