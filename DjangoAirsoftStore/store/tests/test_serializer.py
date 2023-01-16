
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import blasters, UserBlasterRelation
from store.serializers import BlastersSerializer
from rest_framework.test import APITestCase


class BlastersSerializerTestCase(APITestCase):
    def test_srlzr(self):
        user1 = User.objects.create(username='TestUser1', first_name='Vasya', last_name='Pupkin')
        user2 = User.objects.create(username='TestUser2', first_name='Ivan', last_name='Ivanov')
        user3 = User.objects.create(username='TestUser3', first_name='Petya', last_name='Petrov')

        blaster1 = blasters.objects.create(name='Test_blaster1', price=1200, manufacturer='Manufacturer1',
                                           owner=user1)

        blaster2 = blasters.objects.create(name='Test_blaster2', price=2800, manufacturer='Manufacturer2',
                                           owner=user1)

        UserBlasterRelation.objects.create(user=user1, blaster=blaster1, like=True, rate=5)
        UserBlasterRelation.objects.create(user=user2, blaster=blaster1, like=True, rate=5)
        user_blaster_3 = UserBlasterRelation.objects.create(user=user3, blaster=blaster1, like=True)
        user_blaster_3.rate = 4
        user_blaster_3.save()
        user_blaster_3.refresh_from_db()

        UserBlasterRelation.objects.create(user=user1, blaster=blaster2, like=True, rate=3)
        UserBlasterRelation.objects.create(user=user2, blaster=blaster2, like=True, rate=4)
        UserBlasterRelation.objects.create(user=user3, blaster=blaster2, like=False)

        blastersobjects = blasters.objects.all().annotate(annotated_likes=Count(Case(
            When(userblasterrelation__like=True, then=1)))).order_by('id')
        data = BlastersSerializer(blastersobjects, many=True).data
        expected_data = [
            {
                'id': blaster1.id,
                'name': 'Test_blaster1',
                'price': '1200.00',
                'manufacturer': 'Manufacturer1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'TestUser1',
                'watched': [
                    {
                        'first_name': 'Vasya',
                        'last_name': 'Pupkin'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Ivanov'
                    },
                    {
                        'first_name': 'Petya',
                        'last_name': 'Petrov'
                    }
                ]
            },
            {
                 'id': blaster2.id,
                 'name': 'Test_blaster2',
                 'price': '2800.00',
                 'manufacturer': 'Manufacturer2',
                 'annotated_likes': 2,
                 'rating': '3.50',
                 'owner_name': 'TestUser1',
                 'watched': [
                     {
                         'first_name': 'Vasya',
                         'last_name': 'Pupkin'
                     },
                     {
                         'first_name': 'Ivan',
                         'last_name': 'Ivanov'
                     },
                     {
                         'first_name': 'Petya',
                         'last_name': 'Petrov'
                     }
                 ]
             },
        ]
        self.assertEqual(expected_data, data)