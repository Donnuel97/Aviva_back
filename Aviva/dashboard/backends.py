import hashlib  # Add this line to import hashlib

from django.contrib.auth.backends import ModelBackend
from .models import AllUsers
from django.contrib.auth.hashers import check_password

class LegacyDatabaseBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = AllUsers.objects.get(email=email)

            # Calculate the MD5 hash of the provided password
            provided_md5_hash = hashlib.md5(password.encode()).hexdigest()

            # Check if the provided MD5 hash matches the legacy MD5 hash
            if provided_md5_hash == user.password:
                return user
        except AllUsers.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return AllUsers.objects.get(pk=userid)
        except AllUsers.DoesNotExist:
            return None
