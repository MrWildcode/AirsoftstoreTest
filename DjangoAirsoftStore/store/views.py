from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from store.models import blasters, UserBlasterRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BlastersSerializer, UserBlasterRelationSerializer


class BlastersViewSet(ModelViewSet):
    queryset = blasters.objects.all().annotate(annotated_likes=Count(Case(
            When(userblasterrelation__like=True, then=1)))).select_related('owner').prefetch_related('watched').order_by('id')
    serializer_class = BlastersSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] #сначала определяем фильтр backends и наполняем его списком фильтров
    #для фильтрации, поиска и сортировки
    filterset_fields = ['price'] #По каким полям фильтровать
    search_fields = ['name', 'manufacturer']
    ordering_fields = ['price', 'manufacturer']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

class UserBlasterRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBlasterRelation.objects.all()
    serializer_class = UserBlasterRelationSerializer
    lookup_field = 'blastertoget'

    def get_object(self):
        obj, _ = UserBlasterRelation.objects.get_or_create(user=self.request.user,
                                                           blaster_id=self.kwargs['blastertoget'])
        return obj



def oauth(request):
    return render(request, 'oauth.html')

