# mybatch
A simple Python script for easily submitting jobs to an HPC cluster

Copyright 2019-2025 Eelke Spaak, Donders Institute, Nijmegen
Licensed under GPLv3

Use as:

`mybatch.runbatch('--time=00:10:00 --mem=4gb', 'mymodule', 'myfunction', range(10), power=3)`

(Specify backend with kwarg backend='slurm' (default) or backend='torque'.)

to execute mymodule.myfunction 10 times with arguments 0-9, and kwarg power=3.
Multiple arguments are supported (each iterable needs to be of the same length),
and multiple kwargs as well (kwargs are passed as-is to each job).

2nd example to understand multiple argument lists:

`mybatch.runbatch('--time=00:10:00 --mem=4gb', 'mymodule', 'computeproduct', [1,2,3], [4,5,6])`

will launch computeproduct(1,4), computeproduct(2,5), and computeproduct(3,6).

You can specify a logdir for stderr and stdout logs of the jobs, by default this
is `<userhome>/.pythonjobs/<timestamp>`.

Note mybatch.runbatch does not capture job output. It is recommended to have all job output
go via disk. The same goes for elaborate job input. mybatch.runbatch will print job argumenst
into text, so it's recommended to only use numbers (for kwargs, strings will work).

Note furthermore that the requirements string (first argument) has to be specified
in a scheduler-dependent manner. This means '--time=... --mem=...' for Slurm, and
'walltime=...,mem=...' for Torque.
