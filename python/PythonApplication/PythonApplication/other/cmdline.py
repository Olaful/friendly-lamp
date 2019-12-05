import os
from subprocess import Popen

# test case as module
ut_run = 'python -m unittest other.ut'
ut_run = 'python -m unittest other.ut.YourClass'
ut_run = 'python -m unittest other.ut.YourClass.YourMethod'
# more detail info
ut_run_v = 'python -m unittest -v other.ut'
ut_run_b = 'python -m unittest -b other.ut'

# test discover
dc_run = 'python -m unittest discover -s other -p "*t.py"'

if __name__ == '__main__':
    os.chdir(r'..')
    Popen(ut_run_v, stdout=None, stderr=None, shell=True)