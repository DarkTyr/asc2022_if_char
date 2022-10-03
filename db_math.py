import numpy as np

'''Convert dBm power to mW power'''
def dBm_mW(x_dBm:float) -> float:
    return 10**(x_dBm/10)

'''Convert mW power to dBm power'''
def mW_dBm(x_mW:float) -> float:
    return 10*np.log10(x_mW)

'''Add to powers together given in dBm'''
def add_dBm(x_dBm:float, y_dBm:float) -> float:
    sum_mW = dBm_mW(x_dBm) + dBm_mW(y_dBm)
    return mW_dBm(sum_mW)

'''Subtract two powers given in dBm'''
def sub_dBm(x_dBm:float, y_dBm:float) -> float:
    sum_mW = dBm_mW(x_dBm) - dBm_mW(y_dBm)
    return mW_dBm(sum_mW)
