# merge-request-description-generator
A tool for creating merge request description from commit messages

## Features
- Summarize commits in a git branch and generate a merge request description based on them
- Emojis

## Example output
Default
```
================================
Active branch: test
Target branch: main

"Removed unused code for cleanup. Added music sync feature to Bye Bye Bye functionality." 

"Implemented hotdog model for database integration."
================================
```

With emojis
```
================================
Active branch: test
Target branch: main

"Removed unused code 🚮
Added music sync for Bye Bye Bye 🎵
Created Hotdog model 🌭"
================================
``` 

## Usage
### Prerequisites
- [Ollama](https://ollama.com/), either running on local or access to a remote server
- [llama3.1](https://ollama.com/library/llama3.1) model installed with Ollama
- [git](https://git-scm.com/) installed

### Install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generate description
#### Try in the current repo
- Create  and checkout a branch, then make some dummy commits
- run ``` python3 main.py ```

#### Try in another repo
- You can generate an executable, e. g. using [PyInstaller](https://pyinstaller.org/en/stable/)
- Ensure you are in a directory initialized with git
- Run the generated program

### Options
```
usage: merge-request-description-generator [-h] [-e] [-t TARGET_BRANCH] [-o OLLAMA]

options:
  -h, --help            show this help message and exit
  -e, --emoji           enable inserting emojis into the description
  -t TARGET_BRANCH, --target-branch TARGET_BRANCH
                        the merge request's target branch
  -o OLLAMA, --ollama OLLAMA
                        the host of the ollama instance
```
