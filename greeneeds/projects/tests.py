from django.test        import TestCase, Client
from freezegun          import freeze_time
from projects.models    import Category, Project, ProjectImage, Organization
from users.models       import User

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