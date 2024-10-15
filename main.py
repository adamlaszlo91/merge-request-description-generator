import argparse
from typing import Any, Iterator, Mapping
import git
import ollama


def get_commit_messages(repo: git.Repo, active_branch: str, target_branch: str) -> list:
    commit_messages = []
    for commit in repo.iter_commits(f'{target_branch}..{active_branch}'):
        commit_messages.append(commit.message)
    return commit_messages


# TODO: Make ollama url a parameter
# TODO: Add some error handling

def generate_description(commit_messages: list, emoji: bool) -> Iterator[Mapping[str, Any]]:
    emoji_prompt = ' Use emojis.' if emoji else ''
    commit_message_str = '\n========\n'.join(commit_messages)
    return ollama.chat(
        model='llama3.1',
        options={
            'temperature': 0
        },
        messages=[{'role': 'system', 'content': f'You are a merge request description generator. You are given commit messages and you answer only with the generated description. Be concise.{emoji_prompt}'},
                  {'role': 'user', 'content': commit_message_str}],
        stream=True,
    )


def main():
    parser = argparse.ArgumentParser(
        prog='merge-request-description-generator')
    parser.add_argument('-e', '--emoji',
                        action='store_true')
    args = parser.parse_args()

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
    for chunk in generate_description(commit_messages=commit_messages, emoji=args.emoji):
        print(chunk['message']['content'], end='', flush=True)
    print()
    print('=' * 32)


if __name__ == '__main__':
    main()
