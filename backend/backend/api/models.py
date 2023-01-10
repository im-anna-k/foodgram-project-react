from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.username = extra_fields.get('username', '')
        user.last_name = extra_fields.get('last_name', '')
        user.first_name = extra_fields.get('first_name', '')
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Логин', unique=True, max_length=150, blank=True
    )
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    is_staff = models.BooleanField('Сотрудник', default=False)
    is_active = models.BooleanField('Активирован', default=True)
    is_suspended = models.BooleanField('Заблокирован', default=False)
    date_joined = models.DateTimeField(
        'Дата регистрации', default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            full_name = f'{self.first_name} {self.last_name}'
        else:
            full_name = None
        return full_name


class SubscribingAuthors(models.Model):
    """
    Подписка на авторов
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subscribing_authors = models.ManyToManyField(
        CustomUser,
        verbose_name='Список избранного',
        related_name='subscribing_authors',
    )


class Tag(models.Model):
    name = models.CharField('Название', max_length=150, unique=True)
    color = models.CharField('Цветовой HEX-код', max_length=8, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=150)
    measurement_unit = models.CharField('Единицы измерения', max_length=150)


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField('Кол-во')


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(upload_to='recipe_image')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        IngredientForRecipe, verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.IntegerField('Время приготовления в минутах')


class FavoritesList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    favorites_list = models.ManyToManyField(Recipe, blank=True)


class ShoppingList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shopping_list = models.ManyToManyField(Recipe, blank=True)
