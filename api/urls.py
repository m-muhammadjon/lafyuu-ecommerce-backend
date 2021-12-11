from django.urls import path

from . import views

urlpatterns = [
    path('user-create/', views.user_create),
    path('user-login/', views.user_login),
    path('get-user/', views.get_user),
    path('user-update/', views.user_update),
    path('password-change/', views.update_password),

]