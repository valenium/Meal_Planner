from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

MEAL_TYPE = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(help_text='email address', unique=True, error_messages={'unique': 'A user with that email already exists.'})
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
class CollabGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser)
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
class Recipes(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    collab_group = models.ForeignKey(CollabGroup, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['title', 'ingredients', 'instructions']

    def __str__(self):
        return self.title    

class Meal(models.Model):
    type = models.CharField(max_length=1, choices=MEAL_TYPE, default=MEAL_TYPE[0][0])
    date = models.DateField()
    recipe = models.ForeignKey(Recipes, on_delete=models.PROTECT)
    collab_group = models.ForeignKey(CollabGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type[1]} {self.date}"