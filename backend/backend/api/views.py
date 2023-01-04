from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from api.models import CustomUser, SubscribingAuthors, Tag, Ingredient, IngredientForRecipe, Recipe
from api.serializer import TagSerializers, IngredientSerializers, IngredientForRecipeSerializers, \
    IngredientCreateSerializers, RecipeCreateSerializers
from django.shortcuts import get_object_or_404


class TagList(ListAPIView):
    """Получить список Тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class TagGet(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    lookup_field = 'id'


class IngredientsList(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers

    def list(self, request, *args, **kwargs):
        if request.GET.get('name') is None:
            data = self.get_serializer(self.get_queryset(), many=True)
        elif Ingredient.objects.filter(name=request.GET.get('name')).exists():
            data = self.get_serializer(Ingredient.objects.get(name=request.GET.get('name')))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=data.data, status=status.HTTP_200_OK)


class IngredientGet(RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    lookup_field = 'id'


class CreateRecipe(ListAPIView, APIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializers
    lookup_field = 'id'

    def post(self, request):
        ingredients = []
        for el in request.data.get('ingredients'):
            ingredient = get_object_or_404(Ingredient, id=int(el.get('id')))
            ingredient_for_recipe = IngredientForRecipe(
                ingredient=ingredient,
                amount=el.get('amount')
            )
            ingredient_for_recipe.save()
            ingredients.append(ingredient_for_recipe.id)
        data = {
            'author': request.user.id,
            'name': request.data.get('name'),
            'image': request.data.get('image'),
            'text': request.data.get('text'),
            'ingredients': ingredients,
            'tags': request.data.get('tags'),
            'cooking_time': request.data.get('cooking_time')
        }
        serializers = RecipeCreateSerializers(data=data)
        if serializers.is_valid():
            return Response(status=status.HTTP_200_OK, data=serializers.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializers.errors)


class RecipeLict(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializers
    lookup_field = 'id'
