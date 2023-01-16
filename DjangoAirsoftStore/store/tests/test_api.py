import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import blasters, UserBlasterRelation
from store.serializers import BlastersSerializer
from django.test.utils import CaptureQueriesContext


class BlastersApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.blaster1 = blasters.objects.create(name='TestBlaster1', price='4200.00',
                                                manufacturer='Vendor1', owner=self.user)
        self.blaster2 = blasters.objects.create(name='TestBlaster2', price='2800.00',
                                                manufacturer='Vendor3', owner=self.user)
        self.blaster3 = blasters.objects.create(name='TestBlaster3 Vendor3', price='3100.00',
                                                manufacturer='Vendor3', owner=self.user)
        pass


    def test_get(self):
        url = reverse('blasters-list') #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
        blastersset = blasters.objects.all().annotate(annotated_likes=Count(Case(
            When(userblasterrelation__like=True, then=1)))).order_by('id')
        serializer_data = BlastersSerializer(blastersset, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('blasters-list') #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        response = self.client.get(url, data={'search': 'Vendor3'})
        blastersset = blasters.objects.filter(id__in=[self.blaster2.id, self.blaster3.id]).annotate(annotated_likes=Count(Case(
            When(userblasterrelation__like=True, then=1)))).order_by('id')
        serializer_data = BlastersSerializer(blastersset, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('blasters-list') #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        response = self.client.get(url, data={'ordering': 'price'})
        blastersset = blasters.objects.filter(id__in=[self.blaster2.id, self.blaster3.id, self.blaster1.id]).annotate(
            annotated_likes=Count(Case(
                When(userblasterrelation__like=True, then=1)))).order_by('price')
        serializer_data = BlastersSerializer(blastersset, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        db_objects_count = blasters.objects.all().count()
        url = reverse('blasters-list') #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'name': 'M110',
            'price': '2400.00',
            'manufacturer': 'ARES'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(db_objects_count + 1, blasters.objects.all().count())
        self.assertEqual(blasters.objects.last().owner, self.user)

    def test_update(self):
        url = reverse('blasters-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'name': self.blaster1.name,
            'price': '2700.00',
            'manufacturer': self.blaster1.manufacturer
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.blaster1.refresh_from_db()
        self.assertEqual(float(self.blaster1.price), float(data['price']))

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('blasters-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'name': self.blaster1.name,
            'price': '2700.00',
            'manufacturer': self.blaster1.manufacturer
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(float(blasters.objects.first().price), float(self.blaster1.price))

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('blasters-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'name': self.blaster1.name,
            'price': '2700.00',
            'manufacturer': self.blaster1.manufacturer
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.blaster1.refresh_from_db()
        self.assertEqual(float(blasters.objects.first().price), float(self.blaster1.price))

class BlasterRelationTestCase (APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.blaster1 = blasters.objects.create(name='TestBlaster1', price='4200.00',
                                                manufacturer='Vendor1', owner=self.user)
        self.blaster2 = blasters.objects.create(name='TestBlaster2', price='2800.00',
                                                manufacturer='Vendor3', owner=self.user)
        pass


    def test_like(self):
        url = reverse('userblasterrelation-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBlasterRelation.objects.get(user=self.user, blaster=self.blaster1)
        self.assertTrue(relation.like)

    def test_inwishlist(self):
        url = reverse('userblasterrelation-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'in_wishlist': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBlasterRelation.objects.get(user=self.user, blaster=self.blaster1)
        self.assertTrue(relation.in_wishlist)

    def test_rate(self):
        url = reverse('userblasterrelation-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBlasterRelation.objects.get(user=self.user, blaster=self.blaster1)
        self.assertEqual(data['rate'], relation.rate, response.data)

    def test_rate_wrong(self):
        url = reverse('userblasterrelation-detail', args=(self.blaster1.id,)) #по полю name urlpattern объекта вернет ссылку в формате /prefix/
        data = {
            'rate': 12,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, f'Error occured, please'
                                                                   f'see the details: {response.data}')
