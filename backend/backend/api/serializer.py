from api.models import Ingredient, IngredientForRecipe, Recipe, Tag
from rest_framework import serializers


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"

    def validate(self, data):
        for el in data.get("ingredients", []):
            if el.amount < 1.0:
                raise serializers.ValidationError(
                    {
                        "amount":
                            "Убедитесь, что это значение больше либо равно 1."
                    }
                )
        return data


class RecipeForShoppingList(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class IngredientForRecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IngredientForRecipe
        fields = ("ingredient", "amount")
