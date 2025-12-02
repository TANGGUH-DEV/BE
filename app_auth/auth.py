# auth/firebase_auth.py
from rest_framework import authentication, exceptions
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

cred_path = r"D:\portfolio\backend\sistem\serviceAccountKey.json"
cred = credentials.Certificate(cred_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        id_token = request.headers.get("Authorization")
        if not id_token:
            return None  # tidak ada token

        if id_token.startswith("Bearer "):
            id_token = id_token[7:]  # hapus prefix 'Bearer '

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            # buat objek user sementara
            from django.contrib.auth.models import AnonymousUser, User
            user, _ = User.objects.get_or_create(username=uid)
            return (user, None)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Firebase ID token")
