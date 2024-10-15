import argparse
from typing import Any, Iterator, Mapping
import git
import ollama


def get_commit_messages(repo: git.Repo, active_branch: str, target_branch: str) -> list:
    commit_messages = []
    for commit in repo.iter_commits(f'{target_branch}..{active_branch}'):
        commit_messages.append(commit.message)
    return commit_messages


def generate_description(host: str, commit_messages: list, emoji: bool) -> Iterator[Mapping[str, Any]]:
    if not commit_messages:
        return [{'message': {'content': 'No commits found.'}}]

    emoji_prompt = ' Use emojis.' if emoji else ''
    commit_message_str = '\n========\n'.join(commit_messages)
    client = ollama.Client(host=host)
    return client.chat(
        model='llama3.1',
        options={
            'temperature': 0
        },
        messages=[{'role': 'system', 'content': f'You are a merge request description generator. You are given commit messages, summarize them and you answer only with the generated description. Be concise.{emoji_prompt}'},
                  {'role': 'user', 'content': commit_message_str}],
        stream=True,
    )


def main():
    #  Init argument parser
    parser = argparse.ArgumentParser(
        prog='merge-request-description-generator')
    parser.add_argument('-e', '--emoji',
                        action='store_true', help='enable inserting emojis into the description')
    parser.add_argument('-t', '--target-branch',
                        default='main', help='the merge request\'s target branch')
    parser.add_argument('-o', '--ollama',
                        default='localhost', help='the host of the ollama instance')
    args = parser.parse_args()

    # Generate description
    repo = git.Repo('.')
    active_branch = repo.active_branch.name
    target_branch = args.target_branch

    print('=' * 32)
    print(f'Active branch: {active_branch}')
    print(f'Target branch: {target_branch}')
    print()
    commit_messages = get_commit_messages(
        repo=repo, active_branch=active_branch, target_branch=target_branch)
    for chunk in generate_description(host=args.ollama, commit_messages=commit_messages, emoji=args.emoji):
        print(chunk['message']['content'], end='', flush=True)
    print()
    print('=' * 32)


if __name__ == '__main__':
    main()
