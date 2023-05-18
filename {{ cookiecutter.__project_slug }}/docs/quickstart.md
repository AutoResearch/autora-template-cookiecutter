# Quickstart Guide

You will need:

- `python` 3.8 or greater: [https://www.python.org/downloads/](https://www.python.org/downloads/)

*{{ cookiecutter.__contribution_name }} is a part of the `autora` package:

```shell
pip install -U autora["{{ cookiecutter.__full_name }}"]
```


Check your installation by running:
```shell
python -c "from autora.{{ cookiecutter.__full_path.lower().replace('/','.') }} import Example"
```
