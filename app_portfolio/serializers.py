
from rest_framework import serializers
from app_media.serializers import MediaSerializer

from .models import PortfolioUser
class PortfolioUserSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)  # nested media
    class Meta:
        model = PortfolioUser
        fields = ['id', 'deskripsi', 'skill', 'github', 'portfolio_link', 'created_at']


