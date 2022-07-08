import json, jwt
from freezegun import freeze_time

from django.test                    import TestCase, Client
from django.test                    import TestCase, Client
from django.conf                    import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models    import User
from projects.models import Category, Organization, Project, ProjectImage
from unittest.mock   import patch, MagicMock

@freeze_time ("2022-07-13")
class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.maxDiff        = None
        User.objects.create(
            id              = 1,
            kakao_id        = 1,
            email           = '@naver.com',
            name            = '',
            nickname        = '너',
            point           = 100000,
            carbon_point    =  0
        )
        Organization.objects.create(
            id              = 1,
            name            = '그린니즈'
        )
        
        Category.objects.create(
            id              = 1,
            name            = '가방',
            image_url       = 'as'
        )

        Project.objects.create(
            id              = 1,
            user_id         = 1,
            category_id     = 1,
            title           = "화이트 버클 숄더백",
            shortcut_title  = "화이트 버클 숄더백",
            summary         = "어깨에도 채식 한 줌",
            total_amount    = 720000,
            price           = 60000,
            thumbnail       = '1',
            pk_uri          = 'whitebucklebag',
            target_amount   = 1000000,
            start_datetime  = '2022-07-07',
            end_datetime    = '2022-12-07',
            pay_end_date    = '2022-12-18',
            settlement_date = '2022-12-08',
            introduction    = '123',
            budget_plan     = '4'
        )
        ProjectImage.objects.create(
            id         = 1,
            project_id = 1,
            image_url  = 'www.ur1.com'
        )

    def tearDown(self):
        ProjectImage.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()
        Project.objects.all().delete()

    def test_getsuccess(self):
        client = Client()
        
        response = client.get('/projects/1')

        self.assertEqual(response.json(),{
            "results":
                {
                    'id'             : 1,
                    'thumbmail'      : '1',
                    'category'       : '가방',
                    'title'          : "화이트 버클 숄더백",
                    'like_count'     : 0,
                    'target_amount'  : 1000000, 
                    'price'          : 60000,
                    'start_datetime' : '2022-07-07',
                    'end_datetime'   : '2022-12-07',
                    'pay_end_date'   : '2022-12-18',
                    'settlement_date': '2022-12-08',
                    'introduction'   : '123',
                    'budget_plan'    : '4',
                    'total_amount'   : 720000,
                    'organizations'  : [],
                    'images'         : [{
                        'id' : 1,
                        'url' : 'www.ur1.com'
                    }],
                    'remain_days'    : 147
                }
            })
        self.assertEqual(response.status_code, 200)

@freeze_time ("2022-07-13")
class ProjectListViewTest(TestCase):
    def setUp(self):
        self.maxDiff        = None
        User.objects.create(
            id              = 1,
            kakao_id        = 1,
            email           = '@naver.com',
            name            = '',
            nickname        = '너',
            point           = 100000,
            carbon_point    =  0
        )
        Category.objects.create(
            id              = 1,
            name            = '가방',
            image_url       = 'as'
        )

        Project.objects.create(
            id              = 1,
            user_id         = 1,
            price           = 1,     
            category_id     = 1,
            title           = "화이트 버클 숄더백",
            summary         = "어깨에도 채식 한 줌",
            start_datetime  = '2022-07-07',
            end_datetime    = '2022-07-07',
            pay_end_date    = '2022-07-07',
            settlement_date = '2022-07-07',
            total_amount    = 720000,
            thumbnail       = '1',
            target_amount   = 720000,
            )
        
    def tearDown(self):
        User.objects.all().delete()
        Project.objects.all().delete()

    def test_getsuccess(self):
        client = Client()

        response = client.get('/projects?order=random')

        self.assertEqual(response.json(),{
            "results":[
            {
                'id'            : 1,
                'thumbnail'     : '1',
                'category'      : '가방',              
                'title'         : "화이트 버클 숄더백",
                'summary'       : "어깨에도 채식 한 줌", 
                'target_amount' : 720000,
                'remain_days'   : -6,
                'date'          : '2022-07-07',
                'total_amount'  : 720000,
                'like_count'    : 0     
            }]})

        self.assertEqual(response.status_code, 200)

class ProjectUploadTest(TestCase):
    def setUp(self):
        User.objects.create(
            id         = 1,
            kakao_id   = 112343434,
            email      = 'test@mail.com',
            nickname   = "test"
        )

        Organization.objects.bulk_create([
            Organization(
                id   = 1,
                name = "클린오션"
            ),
            Organization(
                id   = 2,
                name = "월드피스"
            ),
            Organization(
                id   = 3,
                name = "그린비젼"
            )
        ])

        Category.objects.create(
            id              = 1,
            name            = '가방',
            image_url       = 'as'
        )

        self.token = jwt.encode({'user_id' : 1}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Organization.objects.all().delete()
        Category.objects.all().delete()

    @patch("projects.views.FileUpload")
    def test_success_project_upload_view_post(self, mocked_client):
        client = Client()
        
        class MockedResponse:
            def upload(self, file):
                return 'https://greeneeds.s3.ap-northeast-2.amazonaws.com/img/aaa'
        
        mocked_client.return_value = MockedResponse()

        file    = SimpleUploadedFile(
            "test.png",
            content = b"file_content",
            content_type = 'image/png'
        )
        headers = {
            "HTTP_Authorization" : self.token,
            "content-type" : "multipart/form-data"
        }
        body    = {
            "category"        : 1,
            "title"           : "abc",
            "summary"         : "abc",
            "target_amount"   : 100,
            "start_datetime"  : "2022-07-02",
            "end_datetime"    : "2022-07-02",
            "formData"        : file
        }
        response = client.post(
            "/projects",
            body,
            **headers
        )
        print(response.items)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'PROJECT_CREATED'})