from functools import wraps
from.models import AllUsers
from django.http import JsonResponse
import hashlib

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = AllUsers.objects.get(email=email)

                # Check if the provided password matches the stored MD5 hash
                md5_hash = hashlib.md5(password.encode()).hexdigest()
                if md5_hash == user.password:
                    # Passwords match, authenticate the user
                    request.session['user_id'] = user.userid
                    return view_func(request, *args, **kwargs)

            except AllUsers.DoesNotExist:
                pass  # User not found

            return JsonResponse({'message': 'Login failed'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
