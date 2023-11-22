---
layout: default
title: Python
nav_order: 4
nav_exclude: false
---

# Python

Python is a high-level, interpreted programming language known for its simplicity, readability, and versatility. It's widely used in various fields, from web development to data science and artificial intelligence.
​
To manage the Python version and third party libraries we are using pyenv and Poetry. For the Python project management we use the pyproject.toml configuration file.

`pyenv` is a tool for managing multiple Python versions on a single system. It's especially useful in environments where different projects require different Python versions. Additionally, we are using the `pyenv-virtualenv` plugin.

*<a href="https://realpython.com/intro-to-pyenv/#installing-pyenv" target="_blank">Install link</a>*

`Poetry` is a tool for dependency management and packaging in Python. It's designed to handle project dependencies and package configuration with ease.

*<a href="https://python-poetry.org/docs/" target="_blank">Install link</a>*

`pyproject.toml` is a configuration file for Python projects, introduced in PEP 518 as a means to improve the specification of project build requirements. This file represents a significant shift from the traditional setup.py script, offering a more standardized and straightforward way to manage project metadata and dependencies.

## pyenv Configuration

Use pyenv to create new venv

```zsh
pyenv virtualenv 3.9.12 webinar-slackbot
```

Activate the new venv

```zsh
pyenv activate webinar-slackbot
```

Set the webinar-slackbot version as project local version.

```zsh
pyenv local webinar-slackbot
```

## Poetry Configuration

After the Python environment has been created with pyenv, we install Poetry:

```zsh
python -m pip install -U pip setuptools
python -m pip install poetry
```

## pyproject.toml Configuration

The Python project structure is defined in the file, with main dirs:

```zsh
src
tests
```

The file defines the required and development dependencies that will be managed by Poetry.

The required Python libraries are listed in:

```zsh
[tool.poetry.dependencies]
```

The Python libraries used to support development are listed in:

```zsh
[tool.poetry.dev-dependencies]
```

Additional configuration of dev tools is also defined in the file.

## Install Python Libraries

After Poetry has been installed and the pyproject.toml has been configured, install the libraries with this command:

```zsh
poetry install
```
