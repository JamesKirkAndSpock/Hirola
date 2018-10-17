from functools import wraps
from django.shortcuts import redirect
from django.core.cache import cache


def old_password_required(function=None):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user.is_change_allowed:
            return function(request, *args, **kwargs)
        else:
            return redirect('/old_password')
    return decorator
