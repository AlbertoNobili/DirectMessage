# DirectMessage

## Interpreter: python3.9

## Description 
This is the repository where I store all the scripts regarding the direct messaging app.

## How to set up this project
1. clone the github repository:
   - git clone https://github.com/AlbertoNobili/DirectMessage.git
2. create a virtual environment inside the project folder:
   - python3.9 -m venv .venv
3. activate the venv and download the requirements:
   - source .venv/bin/activate (bash)
   - .venv\Scripts\activate.bat (cmd)
   - pip install -r requirements.txt
4. open Pycharm and set up the "Python3.9 (DirectMessage)" interpreter
5. start coding

## How to create a new project using PyCharm
1. create a new empty repository on github
2. clone the github repository:
   - git clone https://github.com/AlbertoNobili/newRepository.git
3. create a virtual environment inside the project folder:
   - python -m venv venv
4. open Pycharm and set up the "Python3.9 (Computer Vision)" interpreter
5. start coding

## Basic git commands
- If you want to download from server:
   - git pull origin main
- If you want to upload to server:
   - git add -A
   - git commit -m "comment"
   - git push origin main
- If you want the pull to overwrite local changes:
  - git reset --hard
  - git pull origin main
- If you want the pull to remove untracked local files and/or directories:
   - git clean -f -d
   - git pull origin main
- if you want to put apart local changes and then reapply them:
   - git stash
   - ....
   - git stash pop