from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication routes
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-logout/', views.user_logout, name='user-logout'),

    # User model routes
    path('dashboard/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('dashboard/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),

    # Group routes
    path('groups/<int:collabgroup_id>/', views.groups_detail, name='group_detail'),
    path('groups/', views.groups_index, name='group_index'),
    path('groups/create/', views.GroupCreate.as_view(), name='group_create'),
    path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='group_delete'),

    # Recipe routes
    path('groups/<int:collabgroup_id>/recipes/', views.recipes_index, name='recipes_index'),
    path('groups/<int:collabgroup_id>/recipes/<int:recipe_id>/', views.recipes_detail, name='recipes_detail'),
    path('groups/<int:collabgroup_id>/recipes/create', views.RecipeCreate.as_view(), name='recipes_create'),
    path('groups/<int:collabgroup_id>/recipes/<int:pk>/update', views.RecipeUpdate.as_view(), name='recipes_update'),
    path('groups/<int:collabgroup_id>/recipes/<int:pk>/delete', views.RecipeDelete.as_view(), name='recipes_delete'),

    # Meal routes
    path('groups/<int:collabgroup_id>/meals/', views.meal_calendar, name='meal_calendar'),
    path('groups/<int:collabgroup_id>/meals/<int:year>/<int:week>/', views.meal_calendar, name='meal_calendar_with_date'),

]