import rpy2.robjects as robjects

def test_r_installation():
    try:
        robjects.r('x <- 1')
        return True
    except:
        return False

if test_r_installation():
    print("R installation is working properly.")
else:
    print("R installation is not working properly.")