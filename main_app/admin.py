from django.contrib import admin
from .models import CustomUser, CollabGroup, Recipes, Meal

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CollabGroup)
admin.site.register(Recipes)
admin.site.register(Meal)