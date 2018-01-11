from Facilities.utils import *
import numpy as np
from math import *


#learning params:
# 1. Learning Rate (LR)
# 2. Batch sizeW


def LR_divisor (lr, rmse):
    return float(lr*(1/(1+rmse)))

def LR_expoSmoothing(alpha,rmse,Sn):
    Sn2=alpha*rmse+(1-alpha)*Sn
    return Sn2