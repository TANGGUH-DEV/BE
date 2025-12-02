import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
from app_auth.auth import FirebaseAuthentication


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from app_user.serializers import UserProfileSerializer
from app_user.models import UserProfile

import os

import json

cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

if not cred_json:
    raise Exception("FIREBASE_SERVICE_ACCOUNT not set in environment variables")

cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyFirebaseTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not token:
            return Response({"error": "Token tidak ditemukan"}, status=400)
        ###  print("Authorization header:", request.headers.get("Authorization"))
        ###   print("Headers:", request.headers)
        ### print("Token after strip:", token)

        try:
            decoded = auth.verify_id_token(token)
            uid = decoded["uid"]
            email = decoded.get("email")

            try: 
                user = UserProfile.objects.get(uid=uid)
                if email and user.email !=email:
                    user.email  = email
                    user.save()
            except UserProfile.DoesNotExist:

                user = UserProfile.objects.create(uid=uid, email=email)

            serializer = UserProfileSerializer(user)
            return Response({"message": "Token valid", "user": serializer.data, "role": user.role},status=200   )
        

        
        except FirebaseError as e:
            # Ini akan menangkap Token Expired, Invalid Signature, dll.
            print(f"--- FIREBASE AUTH FAILED: {str(e)} ---")
            # Kembalikan 401 karena ini adalah masalah otorisasi/token
            return Response({"error": f"Otentikasi Token Gagal: {str(e)}"}, status=401)
        
        except Exception as e:
            # PENTING: Cetak error ke konsol backend untuk debugging server
            import traceback
            print("--- FIREBASE VERIFICATION FAILED ---")
            print(traceback.format_exc())
            print("------------------------------------")
            return Response({"error": str(e)}, status=401)
