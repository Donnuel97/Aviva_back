from django.shortcuts import redirect

def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'userid' in request.session:
            # User is logged in, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not logged in, redirect to the login page
            return redirect('login')  # Change 'login' to the actual URL name for your login page
    return wrapped_view
