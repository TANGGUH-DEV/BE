from rest_framework import serializers
from .models import UserProfile
from app_media.serializers import MediaSerializer
 
from app_portfolio.serializers import PortfolioUserSerializer



class UserProfileSerializer(serializers.ModelSerializer):
    portfolios = PortfolioUserSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'uid', 'email', 'role', 'name', 'created_at', 'portfolios', 'media']
