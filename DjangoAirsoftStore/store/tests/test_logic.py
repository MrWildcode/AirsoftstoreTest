from django.db.models import Avg
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from store.logic import set_rating
from store.models import blasters, UserBlasterRelation


class SetRatingTestCase(APITestCase):
    def setUp(self):
        user1 = User.objects.create(username='TestUser1', first_name='Vasya', last_name='Pupkin')
        user2 = User.objects.create(username='TestUser2', first_name='Ivan', last_name='Ivanov')
        user3 = User.objects.create(username='TestUser3', first_name='Petya', last_name='Petrov')

        self.blaster1 = blasters.objects.create(name='Test_blaster1', price=1200, manufacturer='Manufacturer1',
                                           owner=user1)

        UserBlasterRelation.objects.create(user=user1, blaster=self.blaster1, like=True, rate=5)
        UserBlasterRelation.objects.create(user=user2, blaster=self.blaster1, like=True, rate=5)
        UserBlasterRelation.objects.create(user=user3, blaster=self.blaster1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.blaster1)
        self.blaster1.refresh_from_db()
        self.assertEqual('4.67', str(self.blaster1.rating))