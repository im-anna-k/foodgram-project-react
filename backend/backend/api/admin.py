from api.models import (CustomUser, FavoritesList, Ingredient,
                        IngredientForRecipe, Recipe, ShoppingList,
                        SubscribingAuthors, Tag)
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ("email", "username")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "favourites")
    list_filter = ("author", "name", "tags")

    def favourites(self, obj):
        result = FavoritesList.objects.all()
        return sum(
            obj.id in el.favorites_list.values_list('id', flat=True)
            for el in result
        )

    favourites.short_description = "Favourites"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


admin.site.register(Tag)

admin.site.register(ShoppingList)

admin.site.register(FavoritesList)

admin.site.register(SubscribingAuthors)

admin.site.register(IngredientForRecipe)
