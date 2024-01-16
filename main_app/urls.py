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
    # path('groups')

]