from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied

import os

# models
from main_app.models import Repository


def register_user(
        username: str, email: str, password: str, first_name: str = None, last_name: str = None
    ) -> User:
    # create the user
    user = User.objects.create_user(username, email, password)
    if first_name is not None: user.first_name = first_name
    if last_name is not None: user.last_name = last_name
    user.save()

    # add the user's directory
    if not os.path.exists(f"/git/{username}"):
        os.mkdir(f"/git/{username}")
    return user


"""
We first try to login using the username, 
if that fails then we try to login 
using the email. 
"""
def login_user(
        request, username: str, password: str
):
    user = authenticate(request, username, password)
    if user is not None:
        login(request, user)
    else:
        raise PermissionDenied("Username / Password are invalid, please try again")
