from django.urls import path, include
from .views import PortfolioUserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-profiles', PortfolioUserViewSet, basename='userprofile')

urlpatterns = [
    
    path('', include(router.urls)), 
]
