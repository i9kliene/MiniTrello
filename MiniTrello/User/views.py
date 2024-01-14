from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.http import HttpResponseBadRequest
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from . import forms
from . import models
from .tokens import account_activation_token, password_reset_token


# Create your views here.
def homePage(request):
    return render(request, "User/home.html")


def aboutPage(request):
    return render(request, "User/about.html")


def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")


def userRegister(request):
    form = forms.CustomUserCreationForm()
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email confirmation
            user.save()
            login(request, user)
            # Send email confirmation
            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string(
                "User/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            messages.info(
                request,
                f"An activation link has been sent to your email address. Please check your inbox and click the activation link to activate your account.",
            )
            return redirect("user-login")
            # login(request, user)
            # next_url = request.GET.get("next", "home")
            # return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                if field == "password2":
                    field = "password"
                field = field.capitalize()
                messages.error(request, "{}: {}".format(field, " ".join(errors)))

    context = {"form": form}
    return render(request, template_name="User/register.html", context=context)


def activate(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("home")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = models.CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("home")
    else:
        return HttpResponseBadRequest("Activation link is invalid!")


def userLogin(request):
    if request.user.is_authenticated:
        return redirect("board-list")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            messages.error(request, f"Usernname OR Password Incorrect.")
    return render(request, "User/login.html")


def resetPassword(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data["email"]
            for user in form.get_users(cleaned_data):
                current_site = get_current_site(request)
                subject = "Password Reset Requested"
                message = render_to_string(
                    "User/password_reset_email.html",
                    {
                        "email": user.email,
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": password_reset_token.make_token(user),
                    },
                )
                email = EmailMessage(subject, message, to=[cleaned_data])
                email.content_subtype = "html"
                email.send()
                messages.info(
                    request,
                    f"An Password Reset link has been sent to this email address.",
                )
                return redirect("user-login")
            else:
                messages.info(
                    request,
                    f"An Password Reset link has been sent to this email address.",
                )
        else:
            for field, errors in form.errors.items():
                field = field.capitalize()
                messages.error(request, "{}: {}".format(field, " ".join(errors)))
    context = {"form": form}
    return render(request, template_name="User/forgot_password.html", context=context)


def password_change(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("home")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = models.CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        form = PasswordChangeForm(user)
        if request.method == "POST":
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.clean_old_password()
                form.clean_new_password2()
                form.save()
                messages.success(
                    request, f"The password has been changed. Login with New Password"
                )
                return redirect("user-login")

            else:
                for field, errors in form.errors.items():
                    field = field.capitalize()
                    messages.error(request, "{}".format(" ".join(errors)))

    else:
        return HttpResponseBadRequest("Activation link is invalid!")
    context = {"form": form}
    return render(request, template_name="User/change_password.html", context=context)
