from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Tag, Ingredient, IngredientForRecipe, Recipe


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug', 'password']


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientForRecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IngredientForRecipe
        fields = ['ingredient', 'amount']
