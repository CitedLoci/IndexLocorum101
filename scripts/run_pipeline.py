# -*- coding: utf-8 -*-
# author: Matteo Romanello, matteo.romanello@gmail.com

"""
Basic command line interface to run the reference extraction pipeline.

Usage:
    pipeline.py init --config=<file>
    pipeline.py do (preproc | ner | relex | ned | all) --config=<file> [--doc=<name> --overwrite]

Options:
    -h, --help              Show this message.
    -V, --version           Show version.
    -c, --config=<file>     The configuration file.
    -o, --overwrite         Whether existing subdirs within `working-dir` should be kept

Example:
     python scripts/run_pipeline.py do preproc --config=scripts/epibau.ini --doc=cities.txt --working-dir=index_vol3
"""

import codecs
import importlib
import logging
import os
import shutil
import sys

from docopt import docopt

from citation_extractor.core import citation_extractor
from citation_extractor.pipeline import do_ner, get_extractor, get_taggers
from citation_extractor.Utils.IO import init_logger

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


global logger


# TODO: move to the codebase
def init_working_dir(path, overwrite=False):
    """Initializes the wowrking directory with required structure."""
    working_directories = {}
    subdirs = ["orig", "txt", "iob", "iob_ne", "json", "xmi"]

    if os.path.exists(path) and overwrite:
        shutil.rmtree(path)

    for subdir in subdirs:

        newdir = os.path.join(path, subdir)
        if overwrite or not os.path.exists(newdir):
            os.makedirs(newdir)
        working_directories[subdir] = newdir

    return working_directories


def initialize(configuration):
    """
    Validate the configuration file + initialize and persist objects (extractor,
    matcher, etc.) + initialize the working directory with subfolders.
    """
    pass


def main(args):

    global logger
    logger = init_logger(loglevel=logging.INFO)

    if args['init']:
            print('Not yet implemented, sorry.')
    elif args['do']:

        # load the configuration file
        config = configparser.ConfigParser()
        config.readfp(open(args['--config']))

        clear_working_dir = args["--overwrite"]
        doc_id = args["--doc"]

        working_dir = os.path.abspath(config.get('general', 'working_dir'))
        logger.info('Current working directory: {}'.format(working_dir))

        if args['preproc']:
            # validate the configuration file for the given task
            dirs = init_working_dir(working_dir, overwrite=clear_working_dir)

            cfg_split_sentences = config.get('preproc', 'split_sentences')
            cfg_abbrevations_file = config.get('preproc', 'abbreviation_list')
            cfg_treetagger_home = config.get('preproc', 'treetagger_home')

            # if no --doc is passed at cli, then all documents in folder
            # are processed, otherwise only that document
            docs_to_process = []
            if doc_id is None:
                docs_to_process = [
                    file
                    for file in os.listdir(dirs['orig'])
                    if '.txt' in file
                ]
            else:
                docs_to_process.append(doc_id)
            logger.info(
                'Following documents will be processed: {}'.format(
                    docs_to_process
                )
            )

            # initialize TreeTagger PoSTaggers
            try:
                pos_taggers = get_taggers(
                    treetagger_dir=cfg_treetagger_home,
                    abbrev_file=cfg_abbrevations_file
                )
            except Exception as e:
                raise e

            # read the list of abbreviations if provided in config file
            try:
                abbreviations = codecs.open(
                    cfg_abbrevations_file
                ).read().split('\n')
            except Exception as e:
                # no big deal: if abbraviations are not there we simply
                # won't use them
                print(e)
                abbreviations = None

            for doc_id in docs_to_process:
                preproc_document(
                    doc_id,
                    inp_dir=dirs['orig'],
                    interm_dir=dirs['txt'],
                    out_dir=dirs["iob"],
                    abbreviations=abbreviations,
                    taggers=pos_taggers,
                    split_sentences=cfg_split_sentences
                )
            return
        elif args['ner']:

            try:
                cfg_storage = os.path.abspath(config.get('general', 'storage'))
            except Exception:
                cfg_storage = None

            cfg_model_name = config.get('ner', 'model_name')
            cfg_settings_dir = config.get('ner', 'model_settings_dir')

            if cfg_settings_dir not in sys.path:
                sys.path.append(str(cfg_settings_dir))

            dirs = init_working_dir(working_dir, overwrite=clear_working_dir)

            docs_to_process = []
            if doc_id is None:
                docs_to_process = [
                    file
                    for file in os.listdir(dirs['iob'])
                    if '.txt' in file
                ]
            else:
                docs_to_process.append(doc_id)


            # use importlib to import the settings
            ner_settings = importlib.import_module(cfg_model_name)

            # check whether a pickle exists
            if cfg_storage:
                pkl_extractor_path = os.path.join(cfg_storage, 'extractor.pkl')

            # if exists load from memory
            if cfg_storage is not None and os.path.exists(pkl_extractor_path):
                extractor = citation_extractor.from_pickle(pkl_extractor_path)
                logger.info(
                    "Extractor loaded from pickle {}".format(
                        pkl_extractor_path
                    )
                )
            # otherwise initialize and train
            else:
                extractor = get_extractor(ner_settings)
                assert extractor is not None

            logger.info(
                "There are {} docs to process".format(len(docs_to_process))
            )
            for doc_id in docs_to_process:
                do_ner(
                    doc_id,
                    inp_dir=dirs["iob"],
                    interm_dir=dirs["iob_ne"],
                    out_dir=dirs["json"],
                    extractor=extractor
                    )
            return


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
