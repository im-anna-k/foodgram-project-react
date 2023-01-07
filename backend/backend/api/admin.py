from django.contrib import admin

from api.models import CustomUser, Recipe, Ingredient, Tag, ShoppingList, FavoritesList, SubscribingAuthors, \
    IngredientForRecipe

admin.site.register(CustomUser)

admin.site.register(Tag)

admin.site.register(Ingredient)

admin.site.register(Recipe)

admin.site.register(ShoppingList)

admin.site.register(FavoritesList)

admin.site.register(SubscribingAuthors)

admin.site.register(IngredientForRecipe)
