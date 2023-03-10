from api.models import (
    CustomUser,
    FavoritesList,
    Ingredient,
    IngredientForRecipe,
    Recipe,
    ShoppingList,
    SubscribingAuthors,
    Tag,
)
from api.pagination import PaginatorDefault
from api.serializer import (
    IngredientSerializers,
    RecipeCreateSerializers,
    RecipeForShoppingList,
    TagSerializers,
    RecipeCreateWithImageSerializers,
)
from django.shortcuts import get_object_or_404
from fpdf import FPDF
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TagList(ListAPIView):
    """Получить список Тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class TagGet(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    lookup_field = "id"


class IngredientsList(APIView):
    def get(self, request, *args, **kwargs):

        if request.GET.get("name") is None:
            data = IngredientSerializers(Ingredient.objects.all(), many=True)
        elif Ingredient.objects.filter(
            name__istartswith=request.GET.get("name")
        ).exists():
            data = IngredientSerializers(
                Ingredient.objects.filter(
                    name__istartswith=request.GET.get("name")
                ),
                many=True,
            )
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=data.data, status=status.HTTP_200_OK)


class IngredientGet(RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    lookup_field = "id"


def get_data_ingredient(
    recipe,
    author,
    subscribing_authors,
    ingredients,
    tags,
    favorites_list,
    shopping_list,
):
    return {
        "id": recipe.get("id"),
        "name": recipe.get("name"),
        "image": recipe.get("image"),
        "text": recipe.get("text"),
        "cooking_time": recipe.get("cooking_time"),
        "author": {
            "email": author.email,
            "id": author.id,
            "username": author.username,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "is_subscribed": author.id in subscribing_authors,
        },
        "ingredients": ingredients,
        "tags": tags,
        "is_favorited": recipe.get("id") in favorites_list,
        "is_in_shopping_cart": recipe.get("id") in shopping_list,
    }


def ingredient_data(ingredient):
    ingredient_for_recipe = get_object_or_404(
        IngredientForRecipe, id=int(ingredient)
    )
    ingredient_temp = ingredient_for_recipe.ingredient
    return {
        "id": ingredient_temp.id,
        "name": ingredient_temp.name,
        "measurement_unit": ingredient_temp.measurement_unit,
        "amount": ingredient_for_recipe.amount,
    }


def get_lists(request):
    if not request.user.is_authenticated:
        return None, None, None
    subscribing_authors = get_object_or_404(
        SubscribingAuthors, user=request.user.id
    ).subscribing_authors.values_list("id", flat=True)
    favorites_list = get_object_or_404(
        FavoritesList, user=request.user.id
    ).favorites_list.values_list("id", flat=True)
    shopping_list = get_object_or_404(
        ShoppingList, user=request.user.id
    ).shopping_list.values_list("id", flat=True)
    return subscribing_authors, favorites_list, shopping_list


def check_filter(
    filter_is_favorite,
    is_in_shopping_cart,
    filter_author,
    filter_tags,
    recipe,
    shopping_list,
    favorites_list,
    author,
    tags,
):
    if filter_is_favorite is not None and (
        filter_is_favorite
        and recipe.get("id") not in favorites_list
        or not filter_is_favorite
        and recipe.get("id") in favorites_list
    ):
        return True
    if is_in_shopping_cart is not None and (
        is_in_shopping_cart
        and recipe.get("id") not in shopping_list
        or not is_in_shopping_cart
        and recipe.get("id") in shopping_list
    ):
        return True
    if filter_author is not None and filter_author != author.id:
        return True
    if filter_tags is not None and filter_tags is not tags:
        return True
    return False


def filters(request):
    filter_is_favorite = (
        int(request.GET.get("is_favorited", 0)) == 1
        if request.GET.get("is_favorited", None) is not None
        else None
    )
    is_in_shopping_cart = None
    if request.GET.get("is_in_shopping_cart", None) is not None:
        is_in_shopping_cart = (
            int(request.GET.get("is_in_shopping_cart", 0)) == 1
        )
    filter_author = (
        int(request.GET.get("author"))
        if request.GET.get("author", None) is not None
        else None
    )
    filter_tags = (
        int(request.GET.get("tags"))
        if request.GET.get("tags", None) is not None
        else None
    )
    return filter_is_favorite, is_in_shopping_cart, filter_author, filter_tags


class CreateRecipe(APIView):
    permission_classes = ()

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ingredients = []
        for el in request.data.get("ingredients", []):
            ingredient = get_object_or_404(Ingredient, id=int(el.get("id")))
            ingredient_for_recipe = IngredientForRecipe(
                ingredient=ingredient, amount=el.get("amount")
            )
            ingredient_for_recipe.save()
            ingredients.append(ingredient_for_recipe.id)
        data = {
            "author": request.user.id,
            "name": request.data.get("name"),
            "image": request.data.get("image"),
            "text": request.data.get("text"),
            "ingredients": ingredients,
            "tags": request.data.get("tags"),
            "cooking_time": request.data.get("cooking_time"),
        }
        serializers = RecipeCreateWithImageSerializers(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(status=status.HTTP_200_OK, data=serializers.data)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializers.errors
            )

    def get(self, request, *args, **kwargs):
        data = []
        subscribing_authors, favorites_list, shopping_list = get_lists(request)
        (
            filter_is_favorite,
            is_in_shopping_cart,
            filter_author,
            filter_tags,
        ) = filters(request=request)
        for recipe in RecipeCreateSerializers(
            Recipe.objects.all(), many=True
        ).data:
            author = get_object_or_404(CustomUser, id=recipe.get("author"))
            tags = [
                TagSerializers(get_object_or_404(Tag, id=int(tag))).data
                for tag in recipe.get("tags")
            ]
            ingredients = [
                ingredient_data(ingredient=ingredient)
                for ingredient in recipe.get("ingredients")
            ]
            if check_filter(
                filter_is_favorite=filter_is_favorite,
                is_in_shopping_cart=is_in_shopping_cart,
                filter_author=filter_author,
                filter_tags=filter_tags,
                recipe=recipe,
                shopping_list=shopping_list,
                favorites_list=favorites_list,
                author=author,
                tags=tags,
            ):
                continue
            data.append(
                get_data_ingredient(
                    recipe=recipe,
                    author=author,
                    subscribing_authors=subscribing_authors,
                    ingredients=ingredients,
                    tags=tags,
                    favorites_list=favorites_list,
                    shopping_list=shopping_list,
                )
            )

        p = PaginatorDefault(data=data, request=request)
        return Response(data=p.str(), status=status.HTTP_200_OK)


class RecipeGet(APIView):
    def get(self, request, id):
        subscribing_authors, favorites_list, shopping_list = get_lists(request)
        recipe = RecipeCreateSerializers(get_object_or_404(Recipe, id=id)).data
        tags = [
            TagSerializers(get_object_or_404(Tag, id=int(tag))).data
            for tag in recipe.get("tags")
        ]
        ingredients = [
            ingredient_data(ingredient=ingredient)
            for ingredient in recipe.get("ingredients")
        ]
        author = get_object_or_404(CustomUser, id=recipe.get("author"))

        data = get_data_ingredient(
            recipe=recipe,
            author=author,
            subscribing_authors=subscribing_authors,
            favorites_list=favorites_list,
            shopping_list=shopping_list,
            ingredients=ingredients,
            tags=tags,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=id)
        update_data = request.data
        ingredients = []
        for el in update_data.get("ingredients", []):
            ingredient_for_recipe = get_object_or_404(
                IngredientForRecipe, id=int(el.get("id"))
            )
            if ingredient_for_recipe.amount == float(el.get("amount")):
                continue
            if float(el.get("amount")) < 1:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "amount": "Убедитесь, что это значение больше либо равно 1."
                    },
                )
            ingredient_for_recipe.amount = float(el.get("amount"))
            ingredient_for_recipe.save()
            ingredients.append(ingredient_for_recipe.id)
        if ingredients:
            update_data["ingredients"] = ingredients
        else:
            update_data.pop("ingredients", None)
        serializers = RecipeCreateSerializers(
            recipe, data=update_data, partial=True
        )
        if not serializers.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializers.errors
            )
        serializers.save()
        recipe = RecipeCreateSerializers(recipe).data
        subscribing_authors, favorites_list, shopping_list = get_lists(request)
        tags = [
            TagSerializers(Tag, id=int(tag)).data for tag in recipe.get("tags")
        ]
        ingredients = [
            ingredient_data(ingredient=ingredient)
            for ingredient in recipe.get("ingredients")
        ]
        author = get_object_or_404(CustomUser, id=recipe.get("author"))
        data = get_data_ingredient(
            recipe=recipe,
            author=author,
            subscribing_authors=subscribing_authors,
            favorites_list=favorites_list,
            shopping_list=shopping_list,
            ingredients=ingredients,
            tags=tags,
        )
        return Response(status=status.HTTP_200_OK, data=data)

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        get_object_or_404(Recipe, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeLict(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializers
    lookup_field = "id"


class ShoppingListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        shopping_list = get_object_or_404(ShoppingList, user=request.user)
        if recipe.id in shopping_list.shopping_list.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Рецепт уже есть в списке покупок"},
            )
        shopping_list.shopping_list.add(recipe)
        data = RecipeForShoppingList(recipe).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        shopping_list = get_object_or_404(ShoppingList, user=request.user)
        if recipe.id not in shopping_list.shopping_list.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Рецепта нет в списке"},
            )
        shopping_list.shopping_list.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shopping_list = get_object_or_404(ShoppingList, user=request.user)
        name = f"media/files/{request.user.username}."
        data = {}
        for recipe in shopping_list.shopping_list.all():
            for ingredient in recipe.ingredients.all():
                if ingredient.ingredient.name in data:
                    data[ingredient.ingredient.name][
                        "amount"
                    ] += ingredient.amount
                else:
                    data[ingredient.ingredient.name] = {
                        "amount": ingredient.amount,
                        "measurement_unit": ingredient.ingredient.measurement_unit,
                    }
        self.get_pdf(data, f"{name}pdf")
        self.get_txt(data, f"{name}txt")
        self.get_csv(data, f"{name}csv")
        return Response(status=200, data=name)

    def get_pdf(self, data, name):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
        pdf.set_font("DejaVu", "", 14)
        pdf.cell(0, 10, txt="Список Покупок", ln=1, align="C")
        for el, value in data.items():
            str_file = (
                f"{el} ({value['measurement_unit']}) - ({data[el]['amount']})"
            )
            pdf.cell(0, 10, txt=str_file, ln=1, align="L")
        pdf.output(name)

    def get_txt(self, data, name):
        with open(name, "w", encoding="utf-8") as f:
            for el, value in data.items():
                f.write(
                    f"{el} ({value['measurement_unit']}) "
                    f"- ({data[el]['amount']})\n"
                )

    def get_csv(self, data, name):
        with open(name, "w", encoding="utf-8") as f:
            string_file = "".join(
                f"{el} ({value['measurement_unit']}) - ({data[el]['amount']}),"
                for el, value in data.items()
            )
            string_file = string_file[:-1]
            f.write(string_file)


class FavoriteCrud(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorites_list = get_object_or_404(FavoritesList, user=request.user)
        if recipe.id in favorites_list.favorites_list.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Рецепт уже есть в избранном"},
            )
        favorites_list.favorites_list.add(recipe)
        data = RecipeForShoppingList(recipe).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorites_list = get_object_or_404(FavoritesList, user=request.user)
        if recipe.id not in favorites_list.favorites_list.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Рецепт не находится в избранном"},
            )
        favorites_list.favorites_list.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribingAuthorsCrud(APIView):
    def get(self, request):
        subscribing_author = get_object_or_404(
            SubscribingAuthors, user=request.user
        )
        data = []
        for el in subscribing_author.subscribing_authors.all():
            recipes = [
                RecipeForShoppingList(recipe).data
                for recipe in Recipe.objects.filter(author=el)
            ]
            data.append(
                {
                    "email": el.email,
                    "id": el.id,
                    "username": el.username,
                    "first_name": el.first_name,
                    "last_name": el.last_name,
                    "is_subscribed": True,
                    "recipes": recipes,
                    "recipes_count": len(recipes),
                }
            )
            p = PaginatorDefault(data=data, request=request)
            return Response(data=p.str(), status=status.HTTP_200_OK)


class SubscribingAuthorsCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        subscribing_authors = get_object_or_404(
            SubscribingAuthors, user=request.user
        )
        if user.id in subscribing_authors.subscribing_authors.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Вы уже подписаны на автора"},
            )
        if user.id == request.user.id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Нельзя подписаться на себя самого"},
            )
        subscribing_authors.subscribing_authors.add(user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        subscribing_authors = get_object_or_404(
            SubscribingAuthors, user=request.user
        )
        if user.id not in subscribing_authors.subscribing_authors.values_list(
            "id", flat=True
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Пользователя нет в списке"},
            )
        if user.id == request.user.id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Нельзя отписаться от себя"},
            )
        subscribing_authors.subscribing_authors.remove(user)
        return Response(status=status.HTTP_201_CREATED)
