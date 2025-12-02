
from rest_framework.response import Response

from app_auth.auth import FirebaseAuthentication

from .models import UserProfile
from .serializers import UserProfileSerializer

from rest_framework import viewsets, permissions

import logging




# KODE UNTUK MEMBUAT USER PROFILE JIKA BELUM ADA
# KODE UNTUK MEMPERBARUI USER PROFILE JIKA SUDAH ADA

logger = logging.getLogger(__name__)

class PortfolioUserViewSet(viewsets.ModelViewSet):
    queryset =UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "uid"                      
    lookup_url_kwarg = "uid" 
    authentication_classes = [FirebaseAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    # Fungsi get_queryset tidak diubah
    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(uid=user.username)

    # Overwrite create() untuk mendapatkan detail error validasi
    def create(self, request, *args, **kwargs):
        # 1. Logging Permintaan Masuk
        logger.info(f"--- POST Request Received ---")
        logger.info(f"Authenticated User UID: {self.request.user.username}")
        logger.info(f"Request Data: {request.data}")
        logger.info(f"-----------------------------")

        serializer = self.get_serializer(data=request.data)
        
        # 2. Cek dan Logging Validasi Serializer
        if not serializer.is_valid():
            logger.error("!!! SERIALIZER VALIDATION FAILED !!!")
            logger.error(f"Validation Errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
        
        # Jika validasi berhasil, panggil perform_create
        self.perform_create(serializer)
        
        # Siapkan respons sukses
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


    # Fungsi perform_create diubah dan ditambahkan logging
    def perform_create(self, serializer):
        user = self.request.user 
        
        # Perbaikan dari masalah sebelumnya: self.request.user adalah objek UserProfile.
        # Kita hanya perlu menggunakannya langsung.
        try:
            user_profile_instance =UserProfile.objects.get(uid =user.username)
            # Pastikan field foreign key adalah 'user', bukan 'user_id'
            serializer.save()
            logger.info(f"PortfolioUser created successfully for user: {user.username}")
        except Exception as e:
            logger.error(f"!!! CRITICAL ERROR in perform_create !!!")
            logger.error(f"Attempted to save with user object: {user}")
            logger.error(f"Database Save Error: {e}")
            # Penting: Jika terjadi error di sini (misal: database down), 
            # error ini tidak akan dikirim sebagai 400 ke frontend, melainkan 500.
            # Tapi logging ini membantu debugging internal.
            raise # Lemparkan kembali error untuk memicu 500 Internal Server Error


