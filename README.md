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
pip install git+git://github.com/mromanello/CitationExtractor.git@36815d0cdb048cbb56aded6fe8c0a55717566e72
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

### 1. Pre-processing

```bash
python scripts/run_pipeline.py do preproc --config=config/project.ini
```

At this point you should have a tokenized and PoS-tagged file at `data/iob/capra2015_introduction.txt` (if you've kept the default project settings).

Try:

```bash
cat data/iob/capra2015_introduction.txt
```

### 2. Named entity recognition

```bash
python scripts/run_pipeline.py do ner --config=config/project.ini
```

At this point you should have a JSON file with entities annotated at `data/json/capra2015_introduction.json` (if you've kept the default project settings).

Try:

```bash
# requires jq, see https://stedolan.github.io/jq/download/
cat data/json/capra2015_introduction.json|jq ".entities"
```

### TBD
