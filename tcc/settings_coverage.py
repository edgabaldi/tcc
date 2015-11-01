from settings_test import *

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=product,account,core,recommender,tcc',
    '--cover-html',
]
