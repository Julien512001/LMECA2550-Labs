import numpy as np
import matplotlib.pyplot as plt

from States import *



def main():

    #######
    # RPM = 37000 : 37
    # RPM = 50000 : 50
    # Ainsi de suite

    RPM = np.array([37, 50, 60, 70, 80, 90, 100])

    for elem in RPM:
        States(Regime=elem)
        

    

    return 0


if __name__ == "__main__":
    main()