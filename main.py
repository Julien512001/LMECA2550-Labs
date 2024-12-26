import numpy as np
import matplotlib.pyplot as plt

from States import *
from Ratios import *
from Performances import *



def main():

    #######
    # RPM = 37000 : 37
    # RPM = 50000 : 50
    # Ainsi de suite

    RPM = np.array([37, 50, 60, 70, 80, 90, 100])
    # States(Regime=37)


    for elem in RPM:
        States(Regime=elem)



    for elem in RPM:
        ratios = Ratios(Regime=elem)
    

    polytropic()
    massFlowRate()

    # TS_diagram()

    return 0


if __name__ == "__main__":
    main()