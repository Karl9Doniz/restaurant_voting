from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'restaurant'

router = routers.DefaultRouter()
router.register('restaurants', views.RestaurantViewSet, basename='restaurant')
router.register('menus', views.MenuViewSet, basename='menu')
router.register('voting', views.VotingResultsViewSet, basename='voting')

urlpatterns = [
    path('', include(router.urls)),
]