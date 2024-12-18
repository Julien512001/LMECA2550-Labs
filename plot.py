import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




def time_plot():
    df = pd.read_csv("Labo_Result_2024_12_13_14_08.txt", sep='\t')
    hour = df.iloc[:, 0].to_numpy()
    minutes = df.iloc[:, 1].to_numpy()
    second = df.iloc[:, 2].to_numpy()
    for i in range(len(second)):
        second[i] = i

    ps2 = df.iloc[:, 3].to_numpy()
    ps3 = df.iloc[:, 4].to_numpy()
    pt3 = df.iloc[:, 5].to_numpy()
    pt4 = df.iloc[:, 6].to_numpy()
    pt5 = df.iloc[:, 7].to_numpy()

    Tt3 = df.iloc[:, 8].to_numpy()
    Tt4 = df.iloc[:, 9].to_numpy()
    Tt5 = df.iloc[:, 10].to_numpy()

    Tt6 = df.iloc[:, 12].to_numpy()

    Thrust = df.iloc[:, 14].to_numpy()
    RPM = df.iloc[:, 15].to_numpy()

    mdot_f = df.iloc[:, 19].to_numpy()
    mdot_f = mdot_f + np.abs(mdot_f[0])

    plt.plot(second, RPM)

    plt.show()

def RPM_plot():
    df = pd.read_csv("DataMean/LabData_meanValues.csv")
    
    RPM = np.array(df['RPM'])
    mdot_f = np.array(df['mdot_f'])
    Thrust = np.array(df['Thrust'])

    plt.figure()
    plt.scatter(RPM, mdot_f)
    plt.plot(RPM, mdot_f)
    plt.grid()

    plt.figure()
    plt.scatter(RPM, Thrust)
    plt.plot(RPM, Thrust)
    plt.grid()

    plt.show()

# time_plot()
RPM_plot()