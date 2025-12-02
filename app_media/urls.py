from django.urls import path, include
from .views import  MediaViewSet, CloudinarySignatureView, PublicMediaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'media', MediaViewSet, basename='media')
router.register(r'public-media', PublicMediaViewSet, basename='publicmedia')

urlpatterns = [
    
    path("cloudinary-signature/", CloudinarySignatureView.as_view(), name="cloudinary-signature"),
    path('', include(router.urls)), 
]
