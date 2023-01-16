from django.db.models import Avg

from store.models import UserBlasterRelation


def set_rating(blaster):
    rating = UserBlasterRelation.objects.filter(blaster=blaster).aggregate(rating=Avg('rate')).get('rating')
    blaster.rating = rating
    blaster.save()