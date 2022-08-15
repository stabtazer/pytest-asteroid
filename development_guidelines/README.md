# DEVELOPMENT GUIDELINES

## pre-commit

Use pre-commit for enforcing various checks before pushing to Git (pre-commit hook).

### Table of content
1. [Installation](#installation)
2. [How to use](#how-to-use)
3. [Documentation](#documentation)

### Installation
To install pre-commit to your system run:

```
$ pip install pre-commit
```
Then verify the installation by checking the version:
```
$ pre-commit --version
```

**_Why not install with poetry instead of pip?_**

_The reason we use pip to install pre-commit is because the git hooks are installed outside of the poetry environment. Pre-commit pulls the dependencies required for each repository to our local development machine. Note that every pre-commit configuration needs to be activated to the related Git repository by using pre-commit install command  (See section below #Activation)._

### Configuration
Configuration is done by using the following files:
- .pre-commit-config.yml
- pyproject.toml
- .flake8

The `.pre-commit-config.yml` configuration file is placed in the root of the project repository. The individual plugin configurations---used by pre-commit--- are gathered in the `pyproject.toml` (also used by poetry). Currently flake8 plugin is not supported, so this plugin configuration should reside in a `.flake8` file.

### How to use
From the root of your local project repository execute the following command:

```
$ pre-commit install
```
Now pre-commit will run automatically on git commit!
The installed hooks will automatically run on the files you commit to Git. For running on all files use the command

```
$ pre-commit run --all-files
```
All installed hooks can be viewed and added in the `.pre-commit-config.yaml` file.


For updating added hooks to the latest version run:
```
$ pre-commit autoupdate
```

### Documentation
Documentation: [pre-commit](https://pre-commit.com/ "pre-commit's HomePage")

---
### Using poetry

This repository uses poetry for dependency management.

Install (recommended):
```
$ curl -sSL https://install.python-poetry.org | python3 -
```

Install using pip:
```
$ pip install poetry
```
Once installed run the following command from the root directory:

```
$ poetry install
```

---
### Using PyTest ###

__Note!__ Before running your tests make sure that Docker Engine or a docker daemon is running on your machine.

Run tests by
```
$ poetry run python -m pytest
```
