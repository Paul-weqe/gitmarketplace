from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'main_app'


urlpatterns = [
    # users
    path('user/register/', views.RegisterUserView.as_view(), name='register-user'),
    path('user/login/', views.LoginView.as_view(), name='login-user'),

    # general
    path('dashboard/', login_required(views.Dashboard.as_view()), name='dashboard'),

    # repository
    path('repository/create/', login_required(views.CreateRepository.as_view()), name='create-repository'),
    path('repositories/', login_required(views.ViewUserRepositories.as_view()), name='view-user-repositories'),
    path('repositories/<int:id>/', views.ViewSingleRepository.as_view(), name='view-repository'),
    # path('repositories/<int:id>/<str:commit_id>/<str:tree_id>', views.ViewSingleRepository.as_view(), name='view-single-repo-with-commit'),

    # view files and directories
    path('repositories/<int:id>/blob/', views.ViewBlob.as_view(), name='view-blob')
]