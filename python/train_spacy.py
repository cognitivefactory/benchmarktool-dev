from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import spacy
from past.builtins import execfile
execfile('data_processing.py')


filename = "../data/my_data"
target = ["cheval"]
label = ["animal"]

#data = create_annoted_data(filename, target, label)
