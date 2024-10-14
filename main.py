from typing import Any, Iterator, Mapping
import git
import ollama


def get_commit_messages(repo: git.Repo, active_branch: str, target_branch: str) -> list:
    commit_messages = []
    for commit in repo.iter_commits(f'{target_branch}..{active_branch}'):
        commit_messages.append(commit.message)
    return commit_messages


# TODO: Make ollama url a parameter
# TODO: Add help
# TODO: Add some error handling
# TODO: Add emoji support

def generate_description(commit_messages: list) -> Iterator[Mapping[str, Any]]:
    # commit_message_str = '\n========\n'.join(commit_messages)
    # TODO: Remove
    commit_message_str = 'Add reference for food\n========\nFix memory error for plane 4\n========\nRemove unused code'
    return ollama.chat(
        model='llama3.1',
        messages=[{'role': 'system', 'content': 'You are a merge request description generator. You are given commit messages and you answer only with the generated description. Be concise.'},
                  {'role': 'user', 'content': commit_message_str}],
        stream=True,
    )


def main():
    repo = git.Repo('.')
    active_branch = repo.active_branch.name
    # TODO: Make target branch a parameter
    target_branch = 'main'
    print('=' * 32)
    print(f'Active branch: {active_branch}')
    print(f'Target branch: {target_branch}')
    print()
    commit_messages = get_commit_messages(
        repo=repo, active_branch=active_branch, target_branch=target_branch)
    for chunk in generate_description(commit_messages=commit_messages):
        print(chunk['message']['content'], end='', flush=True)
    print()
    print('=' * 32)


if __name__ == '__main__':
    main()
