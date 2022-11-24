from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView, ListView
from main_app.forms import *
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from main_app.services import users, repositories as repo_services
from main_app.models import Repository
from datetime import datetime


class RegisterUserView(FormView):
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = '/user/login/'

    def form_valid(self, form):
        data = form.cleaned_data
        if data['password'] == data['password2']:
            user = users.register_user(
                data['username'], data['email'], data['password'], data['first_name'], data['last_name']
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            raise ValidationError("The password must match the confirm password")


class LoginView(FormView):
    template_name = 'login_user.html'
    form_class = LoginForm
    success_url = '/dashboard'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            raise ValidationError("Username and passwords do not match")


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        user_repositories = Repository.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['user_repositories'] = user_repositories
        return context


class CreateRepository(FormView):
    template_name = 'create_repository.html'
    form_class = CreateRepository
    success_url = '/dashboard'

    def form_valid(self, form):
        data = form.cleaned_data
        repo_services.create_repository(data['name'], self.request.user)
        return super().form_valid(form)


class ViewUserRepositories(ListView):
    template_name = 'view_repository.html'
    paginate_by = 50

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)


class ViewSingleRepository(TemplateView):
    template_name = 'single-repository.html'

    def get_context_data(self, **kwargs):
        context = super(ViewSingleRepository, self).get_context_data(**kwargs)
        repository_id = self.kwargs['id']
        commit_id = self.request.GET.get('commit_id')
        path = self.request.GET.get('path')

        context['repository'] = get_object_or_404(Repository, id=repository_id)
        try:
            context['directories'] = repo_services.get_subtrees(repository_id, commit_id=commit_id, tree_path=path)
            context['files'] = repo_services.get_blobs(repository_id, commit_id=commit_id, tree_path=path)
        except ValueError as e:
            context['error'] = 'Repo does not have any files yet'

        if not path:
            context['tree_path'] = ''
        else:
            context['tree_path'] = path

        context['commit_id'] = commit_id
        context['repository_id'] = repository_id
        repository_commits = repo_services.get_all_repo_commits(repository_id)
        context['repository_commits'] = repository_commits
        for commit in repository_commits:
            make_aware(datetime.fromtimestamp(commit.committed_date))
        return context


class ViewBlob(TemplateView):
    template_name = 'view_blob.html'

    def get_context_data(self, **kwargs):
        repository_id = self.kwargs['id']
        commit_id = self.request.GET.get('commit_id')
        blob_path = self.request.GET.get('path')
        blob_name = self.request.GET.get('blob_name')

        context = super(ViewBlob, self).get_context_data(**kwargs)
        context['repository'] = get_object_or_404(Repository, id=repository_id)
        context['repository_id'] = repository_id
        context['blob_path'] = blob_path
        context['blob_name'] = blob_name
        context['commit_id'] = commit_id

        blob = repo_services.get_single_blob(repository_id, blob_name, tree_path=blob_path, commit_id=commit_id)
        blob_content = blob['blob'].data_stream.read()
        context['blob_content'] = blob_content.decode('utf-8')\
            # .encode("windows-1252").decode('utf-8')
        return context


class CreateFile(FormView):
    form_class = CreateRepositoryFile
    template_name = 'create-file.html'
    success_url = ''

    def form_valid(self, form):
        pass

def logout_view(request):
    logout(request)
    return redirect('/user/login')
