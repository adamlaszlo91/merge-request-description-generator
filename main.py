import git

def get_commit_messages(target_branch: str) -> list:
    commit_messages = []
    repo = git.Repo('.')
    active_branch = repo.active_branch
    for commit in repo.iter_commits(f'{target_branch}..{active_branch.name}'):
        commit_messages.append(commit.message)
    return commit_messages

print(get_commit_messages('main'))