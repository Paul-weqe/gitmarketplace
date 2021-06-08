import git

class GitBase:

    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)

    def get_commit(self, commit_id: str = None):
        if commit_id is None:
            return self.repo.commit()
        return self.repo.commit(commit_id)

    """
    we get the working tree for a specific commit. if the commit id is not specified, 
    the latest commit will automatically be used. 
    """
    def get_tree(self, commit_id = None):
        return self.get_commit(commit_id).tree

    def get_blobs(self, path: str = None, commit_id: str = None):
        commit = self.get_commit(commit_id)
        tree = commit.tree
        blobs = []

        if path is None:
            for blob in tree.blobs:
                blobs.append({'blob': blob, 'blob_name': blob.name})
            return blobs

        dirs = path.split("/")
        [dirs.remove(x) for x in dirs if x == ""]  # remove any trailing '/'
        dirs.reverse()
        while len(dirs) != 0:
            directory = dirs.pop()
            for t in tree.trees:
                if t.name == directory:
                    tree = t
                    continue

        for blob in tree.blobs:
            blobs.append({'blob': blob, 'blob_name': blob.name})
        return blobs

    def get_subtrees(self, path: str = None, commit_id: str=None) -> list:
        commit = self.get_commit(commit_id)
        tree = commit.tree
        subtrees = []
        if path is None:
            for subtree in tree.trees:
                subtrees.append({'subtree': subtree, 'directory_name': subtree.name})
            return subtrees

        dirs = path.split("/")
        [dirs.remove(x) for x in dirs if x == ""] # remove any trailing '/'
        dirs.reverse()
        while len(dirs) != 0:
            directory = dirs.pop()
            for t in tree.trees:
                if t.name == directory:
                    tree = t
                    continue

        for subtree in tree.trees:
            subtrees.append({'subtree': subtree, 'directory_name': subtree.name})
        return subtrees

    def get_all_commits(self):
        return list(self.repo.iter_commits())
