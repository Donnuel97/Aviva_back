from django.contrib.auth.backends import ModelBackend
from .models import AllUsers
import hashlib

class LegacyModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AllUsers.objects.get(email=username)
        except AllUsers.DoesNotExist:
            return None

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if hashed_password == user.password:
            return user
        return None
