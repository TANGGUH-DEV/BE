
from django.urls import path, include
from .views import VerifyFirebaseTokenView



urlpatterns = [
    path('verify-token/', VerifyFirebaseTokenView.as_view(), name='verify-token'),

]