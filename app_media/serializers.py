from rest_framework import serializers
from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    file_get_optimized = serializers.SerializerMethodField()
    
    def get_file_get_optimized(self, obj):
        # Contoh sederhana: tambahkan parameter query untuk optimasi
        if not obj.file_url:
            return None
        return obj.file_url.replace("upload/", "upload/f_auto,q_auto/")  # contoh optimasi Cloudinary
    class Meta:
        model = Media
        fields = ['id','title', 'description', 'file_url', 'file_get_optimized','is_delete', 'media_type', 'created_at']

class PublicMediaSerializer(serializers.ModelSerializer):

    file_get_optimized = serializers.SerializerMethodField()
    
    def get_file_get_optimized(self, obj):
        # Contoh sederhana: tambahkan parameter query untuk optimasi
        if not obj.file_url:
            return None
        return obj.file_url.replace("upload/", "upload/f_auto,q_auto/")  # contoh optimasi Cloudinary
    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'file_get_optimized', 'media_type', 'created_at']