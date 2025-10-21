python3 -m venv ENV
./ENV/bin/pip3 install -r src/app/requirements.txt
./ENV/bin/pip3 freeze > src/app/requirements-lock.txt
