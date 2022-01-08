from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('user-create/', views.user_create),
    path('user-login/', views.user_login),
    path('get-user/', views.get_user),
    path('user-update/', views.user_update),
    path('password-change/', views.update_password),
    path('', include(router.urls)),

]