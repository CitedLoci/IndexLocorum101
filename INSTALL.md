## Installation

Create a new virtual environment with the package of your choice (e.g. `pyenv`, `conda`, `pipenv` etc.).

**NB**: the Python version currently supported is 2.7.x (but I'm working on Py3 support!).

```bash
# feel free to pick another name
pyenv virtualenv 2.7.13 IndexLocorum101
```


Activate the virtual environment that you have just created. In `pyenv` it's:

```bash
pyenv activate IndexLocorum101
```

Once activated, install the dependencies:

```bash
pip install -r requirements.txt
```