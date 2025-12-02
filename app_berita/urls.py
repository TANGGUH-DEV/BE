from django.urls import path, include
from .views import  MediaViewSet, CloudinarySignatureView, PubblicMediaViewSetDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'berita-upload', MediaViewSet, basename='berita-upload')
router.register(r'berita', PubblicMediaViewSetDetail, basename='berita')

urlpatterns = [
    
    path("cloudinary-signature/", CloudinarySignatureView.as_view(), name="cloudinary-signature"),
    path('', include(router.urls)), 
]
