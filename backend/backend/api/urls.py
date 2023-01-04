from django.urls import path

from api.views import TagList, TagGet, IngredientsList, IngredientGet, CreateRecipe

urlpatterns = [
    # Tag
    path('api/tags/', TagList.as_view()),
    path('api/tags/<int:id>', TagGet.as_view()),
    # Ингредиенты
    path('api/ingredients/', IngredientsList.as_view()),
    path('api/ingredients/<int:id>/', IngredientGet.as_view()),
    # Рецепты
    path('api/recipes/', CreateRecipe.as_view()),


]
