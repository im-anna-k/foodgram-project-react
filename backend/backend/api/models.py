from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
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
    username = models.CharField('Логин', unique=True, max_length=150, blank=True)
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    is_staff = models.BooleanField('Сотрудник', default=False)
    is_active = models.BooleanField('Активирован', default=True)
    is_suspended = models.BooleanField('Заблокирован', default=False)
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)

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
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )
    subscribing_authors = models.ManyToManyField(
        CustomUser,
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ShoppingList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(Recipe, on_delete=models.CASCADE)
