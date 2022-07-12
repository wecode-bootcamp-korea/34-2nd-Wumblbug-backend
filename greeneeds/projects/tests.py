from django.test        import TestCase, Client

from projects.models    import Project, Category
from users.models       import User

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
