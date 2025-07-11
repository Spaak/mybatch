def myfunction(num, power=2):
    print('mymodule.myfunction called with arguments: num={}, power={}'.format(num, power))
    return num**power

def computeproduct(a, b):
    print('mymodule.computeproduct called with arguments: a={}, b={}'.format(a, b))
    return a*b

def _get_testargs():
    alla = list(range(3))
    allb = list(range(3, 6))
    power = 3

    return alla, allb, power

def test_local():
    alla, allb, power = _get_testargs()
    
    for a in alla:
        myfunction(a, power)
    
    for a, b in zip(alla, allb):
        computeproduct(a, b)

def test_qsub():
    alla, allb, power = _get_testargs()

    import mybatch
    mybatch.qsub('walltime=00:05:00,mem=4gb', 'mymodule', 'myfunction', alla, power=power)
    mybatch.qsub('walltime=00:05:00,mem=4gb', 'mymodule', 'computeproduct', alla, allb)

def test_sbatch():
    alla, allb, power = _get_testargs()

    import mybatch
    mybatch.sbatch('--mem=4gb --time=00:01:00', 'mymodule', 'myfunction', alla, power=power)
    mybatch.sbatch('--mem=4gb --time=00:01:00', 'mymodule', 'computeproduct', alla, allb)