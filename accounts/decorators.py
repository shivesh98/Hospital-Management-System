from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="hr").exists():
                return redirect("hrhome")
            if request.user.groups.filter(name="receptionist").exists():
                return redirect("recephome")
            if request.user.groups.filter(name="doctor").exists():
                return redirect("doctor")
            if request.user.groups.filter(name="patient").exists():
                return redirect("patient")

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator


def hr_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "patient":
            return redirect("patient")

        if group == "doctor":
            return redirect("doctor")

        if group == "hr":
            return view_func(request, *args, **kwargs)

    return wrapper_function


def recep_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "patient":
            return redirect("patient")

        if group == "doctor":
            return redirect("doctor")

        if group == "receptionist":
            return view_func(request, *args, **kwargs)

    return wrapper_function
