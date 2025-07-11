# Copyright 2019 Eelke Spaak, Donders Institute, Nijmegen
# Licensed under GPLv3
#
# Use as:
#
# mybatch.runbatch('walltime=01:00:00,mem=4gb', 'mymodule', 'myfunction', range(10), power=3)
#
# specify backend with kwarg backend='slurm' (default) or backend='torque'
#
# to execute mymodule.myfunction 10 times with arguments 0-9, and kwarg power=3.
# Multiple arguments are supported (each iterable needs to be of the same length),
# and multiple kwargs as well (kwargs are passed as-is to each job).
#
# 2nd example to understand multiple argument lists:
#
# mybatch.runbatch('walltime=00:20:00,mem=4gb', 'mymodule', 'computeproduct', [1,2,3], [4,5,6])
#
# will launch computeproduct(1,4), computeproduct(2,5), and computeproduct(3,6).
#
# You can specify a logdir for stderr and stdout logs of the jobs, by default this
# is <userhome>/.pythonjobs/<timestamp>.
#
# Note mybatch.runbatch does not capture job output. It is recommended to have all job output
# go via disk. The same goes for elaborate job input. mybatch.runbatch will print job argumenst
# into text, so it's recommended to only use numbers (for kwargs, strings will work).

import os
from os.path import expanduser
import numpy as np
from datetime import datetime

def qsub(*args, **kwargs):
    runbatch(*args, backend='torque', **kwargs)

def sbatch(*args, **kwargs):
    runbatch(*args, backend='slurm', **kwargs)

def runbatch(reqstring, module, fun, *args, logdir=None, backend=None, **kwargs):
    if backend is None:
        backend = 'slurm'

    nargs = len(args)
    njob = len(args[0])

    pythoncmd = 'python'

    batchid = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    if logdir is None:
        logdir = expanduser('~/.pythonjobs/')
    batchdir = logdir + batchid
    os.mkdir(batchdir)

    for k, thisargs in enumerate(zip(*args)):
        argslist = ','.join([str(x) for x in thisargs])
        pythonscript = 'import os; os.chdir(\'{}\'); from {} import {}; kwargs={}; {}({}, **kwargs)'.format(os.getcwd(), module,
            fun, kwargs, fun, argslist)

        # escape the python script so that ' is output correctly by echo
        pythonscript = pythonscript.replace("'", "'\\''")
        pythoncmd = 'python -c "{}"'.format(pythonscript)

        # log files
        logfile = '{}/j{}_{}'.format(batchdir, thisargs[0], fun)

        if backend == 'torque':
            # note the -V which ensures the child job inherits the proper environment
            batchcmd = 'qsub -o /dev/null -e /dev/null -V -l {} -N j{}_{}'.format(
                reqstring, thisargs[0], fun)
        elif backend == 'slurm':
            # note --export=ALL to inherit the environment (should be default, but specify still)
            batchcmd = 'sbatch --export=ALL {} -J j{}_{}'.format(
                reqstring, thisargs[0], fun)
        else:
            raise ValueError('unknown backend: ' + backend)

        fullcmd = 'echo \'{} >{}.out 2>{}.err\' | {}'.format(
            pythoncmd, logfile, logfile, batchcmd)

        os.system(fullcmd)
        # print(fullcmd)
