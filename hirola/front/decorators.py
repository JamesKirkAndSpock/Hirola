from functools import wraps
from django.shortcuts import redirect
from django.conf import settings


def old_password_required(function=None):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user.is_change_allowed:
            return function(request, *args, **kwargs)
        else:
            return redirect('/old_password')
    return decorator


def remember_user(function=None):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.POST.get('remember-user'):
            request.session.set_expiry(1209600)
            return function(request, *args, **kwargs)
        return function(request, *args, **kwargs)
    return decorator


def is_change_allowed_required(function=None):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user.is_change_allowed:
            return function(request, *args, **kwargs)
        else:
            return redirect('/confirm_user')
    return decorator


def get_request_inhibit(function=None):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.method == "GET":
            return redirect("/")
        else:
            return function(request, *args, **kwargs)
    return decorator
