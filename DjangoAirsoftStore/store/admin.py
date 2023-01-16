from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import blasters, gear, UserBlasterRelation


@admin.register(blasters)
class BlastersAdmin(ModelAdmin):
    pass

@admin.register(UserBlasterRelation)
class UserBlasterRelationAdmin(ModelAdmin):
    pass

admin.site.register(gear)
