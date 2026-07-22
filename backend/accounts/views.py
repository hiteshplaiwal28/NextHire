from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def register_user(username, email, password):

    # Username already exists
    if User.objects.filter(username=username).exists():
        return False, "Username already exists."

    # Email already exists
    if User.objects.filter(email=email).exists():
        return False, "Email already registered."

    # Create user
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    return True, "Registration successful."


def login_user(username, password):

    user = authenticate(
        username=username,
        password=password,
    )

    if user is None:
        return None

    return user