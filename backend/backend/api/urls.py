from django.urls import path

from api.views import TagList, TagGet, IngredientsList, IngredientGet, CreateRecipe, RecipeGet, ShoppingListCreate, \
    DownloadShoppingList, FavoriteCrud, SubscribingAuthorsCrud, SubscribingAuthorsCreate

urlpatterns = [
    # Теги
    path('api/tags/', TagList.as_view()),
    path('api/tags/<int:id>', TagGet.as_view()),
    # Ингредиенты
    path('api/ingredients/', IngredientsList.as_view()),
    path('api/ingredients/<int:id>/', IngredientGet.as_view()),
    # Рецепты
    path('api/recipes/', CreateRecipe.as_view()),
    path('api/recipes/<int:id>/', RecipeGet.as_view()),
    # Список покупок
    path('api/recipes/<int:id>/shopping_cart/', ShoppingListCreate.as_view()),
    path('api/recipes/download_shopping_cart/', DownloadShoppingList.as_view()),
    # Избранное
    path('api/recipes/<int:id>/favorite/', FavoriteCrud.as_view()),
    # Подписки
    path('api/users/subscriptions/', SubscribingAuthorsCrud.as_view()),
    path('api/users/<int:id>/subscribe/', SubscribingAuthorsCreate.as_view()),
]
