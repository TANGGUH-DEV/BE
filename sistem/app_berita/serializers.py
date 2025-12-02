from rest_framework import serializers
from .models import News
import bleach

class MediaSerializer(serializers.ModelSerializer):
    file_get_optimized = serializers.SerializerMethodField()
    
    def get_file_get_optimized(self, obj):
        # Contoh sederhana: tambahkan parameter query untuk optimasi
        if not obj.thumbnail:
            return None
        return obj.thumbnail.replace("upload/", "upload/f_auto,q_auto/")  # contoh optimasi Cloudinary
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content', 'category',
            'thumbnail', 'file_get_optimized', 'is_published', 'is_delete', 'created_at', 'updated_at']


class PublicMediaSerializer(serializers.ModelSerializer):
    file_get_optimized = serializers.SerializerMethodField()
    
    def get_file_get_optimized(self, obj):
        # Contoh sederhana: tambahkan parameter query untuk optimasi
        if not obj.thumbnail:
            return None
        return obj.thumbnail.replace("upload/", "upload/f_auto,q_auto/")  # contoh optimasi Cloudinary
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content', 'category', 'thumbnail',
            'file_get_optimized', 'created_at', 'updated_at']
        
        
        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"

    def validate_content(self, value):
        allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
            'p','img','br','div','span','strong','em','h1','h2','h3','ul','ol','li'
        ]
        allowed_attrs = {
            '*': ['style'],
            'img': ['src', 'alt'],
        }
        return bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs)