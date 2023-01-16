from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.admin import UserBlasterRelation
from store.models import blasters

class BlasterWatchedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BlastersSerializer(ModelSerializer):
    #likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    watched = BlasterWatchedSerializer(many=True, read_only=True)
    class Meta:
        model = blasters
        fields = ('id','name','price','manufacturer', 'annotated_likes', 'rating', 'owner_name', 'watched')

    # def get_likes_count(self, instance):
    #     return UserBlasterRelation.objects.filter(blaster=instance, like=True).count()
        #вызовет по одному доп запросу в бд для каждого обрабатываемого во view объекта

class UserBlasterRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBlasterRelation
        fields = ('blaster', 'like', 'in_wishlist', 'rate')