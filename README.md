# IndexLocorum101

A template project for those wanting to create an *index locorum* for their publications.

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

## Configuration

This template comes with batteries included, but you will have to adapt a bit the configuration. The project configuration file is in [`config/project.ini`](config/project.ini).

Make sure you change the path for the following settings:
- `preproc.treetagger_home`: the path to `TreeTagger`

## Data preparation

This template project comes with an example document, the introduction of Andrea Capra's book [*Plato's Four Muses: The Phaedrus and the Poetics of Philosophy*](http://nrs.harvard.edu/urn-3:hul.ebook:CHS_CapraA.Platos_Four_Muses.2014).

The documents to be processed need to be placed in the sub-folder `orig` within your working directory.

In this example project `general.working_dir = ./data`, thus the input files are placed in `./data/orig/`. The script will then create further subfolders to store temporary or intermediate files.

## Running the pipeline

### Pre-processing

```bash
python scripts/run_pipeline.py do preproc --config=config/project.ini
```

### Named entity recognition

```bash
python scripts/run_pipeline.py do ner --config=config/project.ini
```

### TBD
