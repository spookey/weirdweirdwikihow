from os import path

NAME_APP = 'weirdweirdwikihow'

DIR_LIB = path.abspath(path.dirname(__file__))
DIR_SRC = path.abspath(path.dirname(DIR_LIB))
DIR_ROOT = path.abspath(path.dirname(DIR_SRC))

DIR_LOGS = path.join(DIR_ROOT, 'logs')
