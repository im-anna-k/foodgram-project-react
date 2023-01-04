from django.contrib import admin

from api.models import CustomUser, Recipe, Ingredient, Tag

admin.site.register(CustomUser)

admin.site.register(Tag)

admin.site.register(Ingredient)

admin.site.register(Recipe)
