---
layout: default
title: Python
nav_exclude: true
---

## Python

Python is a high-level, interpreted programming language known for its simplicity, readability, and versatility. It's widely used in various fields, from web development to data science and artificial intelligence.

To manage the Python version and third party libraries we are using pyenv and Poetry. For the Python project management we use pyproject.toml configuration file.

`pyenv` is a tool for managing multiple Python versions on a single system. It's especially useful in environments where different projects require different Python versions. Additionally, we are using `pyenv-virtualenv` plugin.

*[Install link](https://realpython.com/intro-to-pyenv/#installing-pyenv)*.

`Poetry` is a tool for dependency management and packaging in Python. It's designed to handle project dependencies and package configuration with ease.

*[Install link](https://python-poetry.org/docs/)*.

`pyproject.toml` file is a configuration file for Python projects, introduced in PEP 518 as a means to improve the specification of project build requirements. This file represents a significant shift from the traditional setup.py script, offering a more standardized and straightforward way to manage project metadata and dependencies.

### pyenv Configuration

Use pyenv to create new venv

```zsh
pyenv virtualenv 3.9.12 webinar-slackbot
```

Activate the new venv

```zsh
pyenv activate webinar-slackbot
```

Set the pyenv version as local for this directory

```zsh
pyenv local webinar-slackbot
```

### Poetry Configuration

After the Python envorioment has been created with pyenv, we install Poetry.

```zsh
python -m pip install -U pip setuptools
python -m pip install poetry
```

### pyproject.toml Configuration

The Python project structure is defined in the file, with main dirs:

```zsh
src
tests
```

The file defines the required and development dependencies that will be managed by Poetry.

The required Python libraries are listed in:

```
[tool.poetry.dependencies]
```

The Python libraries used to support development are listed in:

```
[tool.poetry.dev-dependencies]
```

Additional configuration of dev tools is defines in the file as well.

### Install Python Libraries

After Peotry has been install and the pyproject.toml has been configure, install the libraries with this command:

```zsh
poetry install
```
