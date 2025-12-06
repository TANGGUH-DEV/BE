from rest_framework.views import APIView
from rest_framework.response import Response

from app_auth.auth import FirebaseAuthentication

from .models import  News
from .serializers import PublicMediaSerializer, MediaSerializer

from rest_framework import viewsets, permissions

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

import logging
import time, hashlib
from django.conf import settings

from .pagination import PaginationHandler

from app_user.models import UserProfile

#UNTUK MEDIA UPLOAD 
# UJI COBA DENGAN FRONTEND SETELAH BACKEND BERJALAN

logger = logging.getLogger(__name__)

class MediaViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = MediaSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "slug"          # <- pakai slug
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        """
        Menampilkan hanya media milik user yang sedang login.
        """
        user = self.request.user

        if self.request.method == "GET" and not self.kwargs.get("slug"):
            return News.objects.filter(author__uid=user.username, is_delete=False)

        return News.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Logging + validasi saat membuat media baru.
        """
        logger.info("=== POST Request: Create Media ===")
        logger.info(f"Authenticated user: {self.request.user.username}")
        logger.info(f"Data diterima: {request.data}")

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("VALIDATION FAILED")
            logger.error(serializer.errors)
            return Response(serializer.errors, status=400)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        """
        Menyimpan media dan mengaitkannya dengan user yang sedang login.
        """
        user = self.request.user
        try:
            user_profile_instance = UserProfile.objects.get(uid=user.username)
            serializer.save(author=user_profile_instance)
            logger.info(f"✅ Media berhasil disimpan untuk user: {user.username}")
        except Exception as e:
            logger.error("!!! ERROR saat menyimpan media !!!")
            logger.error(str(e))
            raise

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: tandai media sebagai dihapus tanpa menghapus dari database.
        """
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        logger.info(f"Media id={instance.id} ditandai sebagai dihapus oleh user {request.user.username}")
        return Response(status=204)

#API publik untuk 
@method_decorator(cache_page(60), name="dispatch")
class PublicMediaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Menyediakan endpoint publik untuk melihat media.
    Hanya menampilkan media dengan media_type 'public'.
    """
    queryset = News.objects.filter(is_delete=False)
    serializer_class = PublicMediaSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PaginationHandler
    http_method_names = ['get']


@method_decorator(cache_page(60), name="dispatch")
class PubblicMediaViewSetDetail(viewsets.ReadOnlyModelViewSet):

    """
    Menyediakan endpoint untuk detail berita yang ditampilkan
    berdasarkan slug yang ada
    """
    queryset = News.objects.filter(is_delete=False)
    serializer_class = PublicMediaSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    http_method_names = ['get']


# SIGNATURE UNTUK UPLOAD KE CLOUDINARY

class CloudinarySignatureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        timestamp = int(time.time())
        # Ambil parameter yang akan diunggah dari query params
        upload_preset = request.query_params.get('upload_preset', 'ml_default')
        folder = request.query_params.get('folder', 'media') 
        
        # 1. SIAPKAN PARAMETER YANG AKAN DITANDATANGANI (DIURUTKAN ALFABETIS)
        params = {
            'timestamp': timestamp,
            'upload_preset': upload_preset,
            'folder': folder,
            # Tambahkan parameter lain jika ada (misalnya public_id)
        }
        
        # 2. KONSTRUKSI STRING UNTUK SHA1 (Key1=Value1&Key2=Value2)
        # Cloudinary TIDAK HANYA menerima timestamp saja.
        sorted_params = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        
        # 3. GABUNGKAN DENGAN API_SECRET
        string_to_sign = f"{sorted_params}{settings.CLOUDINARY_API_SECRET}"
        
        # 4. HITUNG TANDA TANGAN (SIGNATURE)
        signature = hashlib.sha1(string_to_sign.encode('utf-8')).hexdigest()

        return Response({
            "signature": signature,
            "timestamp": timestamp,
            "api_key": settings.CLOUDINARY_API_KEY,
            "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "upload_preset": upload_preset, # Kirim kembali untuk dipakai frontend
            "folder": folder, # Kirim kembali untuk dipakai frontend
        })