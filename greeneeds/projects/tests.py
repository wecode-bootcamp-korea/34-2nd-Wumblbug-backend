from django.test        import TestCase, Client

from projects.models    import Category, Project, ProjectImage, Organization
from users.models       import User

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
        id                  = 1,
        project_id          = 1,
        image_url           = 'https://greeneeds.s3.ap-northeast-2.amazonaws.com/img/bag3.jpg'
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
             'images'         : 'https://greeneeds.s3.ap-northeast-2.amazonaws.com/img/bag3.jpg',
             'remain_days'    : 148
             }})
      
        self.assertEqual(response.status_code, 200)