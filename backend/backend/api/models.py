from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class SubscribingAuthors(models.Model):
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    subscribing_authors = models.ManyToManyField(
        Profile,
        verbose_name='Список избранного',
        related_name='subscribing_authors'
    )


class Tag(models.Model):
    name = models.CharField('Название', max_length=150, unique=True)
    color_hex = models.CharField('Цветовой HEX-код', max_length=8, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class UnitsMeasurement(models.Model):
    name = models.CharField('Название', max_length=150)


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=150)
    units_measurement = models.ManyToManyField(UnitsMeasurement)


class IngredientForRecipe(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    units_measurement = models.OneToOneField(UnitsMeasurement, on_delete=models.CASCADE)
    quantity = models.FloatField('Кол-во')


class Recipe(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(upload_to='recipe_image')
    description = models.TextField('Описание')
    ingredient = models.ManyToManyField(
        IngredientForRecipe,
        verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги')
    time_minute = models.IntegerField('Время приготовления в минутах')


class FavoritesList(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ShoppingList(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(Recipe, on_delete=models.CASCADE)
