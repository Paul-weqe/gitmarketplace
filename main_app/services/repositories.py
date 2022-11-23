from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from main_app.models import Repository
from git import Repo

from main_app.services.git_service import GitBase


def create_repository(
        repository_name: str, user: User
) -> Repository:
    repo_object = Repository(name=repository_name, user=user)
    repo_object.save()

    Repo.init(f"/git/{user.username}/{repository_name}", bare=True)
    return repo_object

def get_blobs(repository_id: int, commit_id: str = None, tree_path: str = None) -> list:
    repository_object = get_object_or_404(Repository, id=repository_id)
    username = repository_object.user.username
    path = f"/git/{username}/{repository_object.name}/"
    base = GitBase(path)
    return base.get_blobs(commit_id=commit_id, path=tree_path)

def get_subtrees(repository_id: int, commit_id: str = None, tree_path: str = None) -> list:
    repository_object = get_object_or_404(Repository, id=repository_id)
    username = repository_object.user.username
    path = f"/git/{username}/{repository_object.name}/"
    base = GitBase(path)
    return base.get_subtrees(commit_id=commit_id, path=tree_path)

def get_single_blob(repository_id: int, blob_name: str, tree_path: str = None, commit_id: str = None):
    blobs = get_blobs(repository_id, commit_id, tree_path)
    for blob in blobs:
        if blob['blob_name'] == blob_name:
            return blob


def get_all_repo_commits(repository_id: int):
    repository_object = get_object_or_404(Repository, id=repository_id)
    username = repository_object.user.username
    path = f"/git/{username}/{repository_object.name}/"
    base = GitBase(path)
    response = None
    try:
        response = base.get_all_commits()
    except ValueError as e:
        if str(e) == "Reference at 'refs/heads/master' does not exist":
            response = []
    return response

