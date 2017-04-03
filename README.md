# siyavula_pyramid


## Getting Started


- These instructions assume that python3.* is installed.

- Change directory into project.

    - cd siyavula_pyramid

- Create a Python virtual environment.

    - python3 -m venv venv

- Upgrade packaging tools.

    - venv/bin/pip install --upgrade pip setuptools

- Install the project with its testing requirements.

    - venv/bin/pip install ".[testing]"

- Install project third party requirements.

    - venv/bin/pip install -r requirements.txt 

- Run tests.

    - venv/bin/pytest

- Run project.

    - venv/bin/pserve production.ini
