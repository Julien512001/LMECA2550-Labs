import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

gamma = 1.4
RPM = np.array([37, 50, 60, 70, 80, 90, 100])
Rstar = 287.058

A1 = 5.168e-3
A2 = 2.818e-3
A3 = 4.112e-3
A4 = 6.323e-3
A5 = 3.519e-3
A6 = 3.318e-3

def polytropic():
    ec = np.zeros(len(RPM))
    eta_c = np.zeros(len(RPM))
    et = np.zeros(len(RPM))
    eta_t = np.zeros(len(RPM))

    for i in range(len(RPM)):
        filename = f"dataR/Ratios/Ratios_RPM{RPM[i]}.csv"
        df = pd.read_csv(filename)

        tau_c, pi_c = df['c']
        tau_t, pi_t = df['t']


        # !!!!! Attention à verifier les équations !!!!!
        ec[i] = (gamma-1)/gamma * np.log(pi_c)/np.log(tau_c)
        eta_c[i] = (pi_c**((gamma-1)/gamma) - 1 )/(tau_c - 1)
        et[i] = gamma/(gamma-1) * np.log(tau_t)/np.log(pi_t)
        eta_t[i] = (1-tau_t)/(1-tau_t**(1/et[i]))
    
    plt.figure()
    plt.scatter(RPM, et)
    plt.plot(RPM, et, label="et")
    plt.scatter(RPM, eta_c)
    plt.plot(RPM, eta_c, label="eta_c")
    plt.scatter(RPM, ec)
    plt.plot(RPM, ec, label='ec')
    plt.scatter(RPM, eta_t)
    plt.plot(RPM, eta_t, label='eta_t')
    plt.ylim(0.0)

    plt.legend()
    plt.grid()


    plt.show()




def massFlowRate():

    mdot_c = np.zeros(len(RPM))
    mdot_t = np.zeros(len(RPM))
    for i in range(len(RPM)):
        filename = f"dataR/States/States_RPM{RPM[i]}.csv"
        df = pd.read_csv(filename)

        state2 = np.array(df['State2'])
        ps = state2[0]
        T = state2[2]
        u = state2[4]
        rho = ps/(Rstar*T)
        mdot_c[i] = rho*u*A2

        state4 = np.array(df['State4'])
        ps = state4[0]
        T = state4[2]
        u = state4[4]
        rho = ps/(Rstar*T)
        mdot_t[i] = rho*u*A4
    
    plt.figure()
    plt.scatter(RPM, mdot_c)
    plt.plot(RPM, mdot_c, label='mdot_c')
    plt.ylim(0.0)
    plt.legend()
    plt.grid()

    plt.figure()
    plt.scatter(RPM, mdot_t)
    plt.plot(RPM, mdot_t, label='mdot_t')
    plt.ylim(0.0)
    plt.legend()
    plt.grid()


    plt.show()


def TS_diagram():
    RPM = np.array([37, 50, 60, 70, 80, 90, 100])
    for i in range(len(RPM)):
        filename = f"dataR/States/States_RPM{RPM[i]}.csv"
        df = pd.read_csv(filename)

        states = np.array(df)
        
        T = np.zeros(7)
        s = np.zeros(7)

        for i in range(len(T)):
            T[i] = states[2, i]
            s[i] = states[5, i]


        plt.figure()
        plt.scatter(s, T)
        plt.plot(s, T)
        for i in range(len(T)):
            plt.text(s[i], T[i], str(i), fontsize=10, color="red", ha="right", va="bottom")

        plt.xlabel("Entropy (s)")
        plt.ylabel("Temperature (T)")
        plt.title(f"Temperature vs Entropy for RPM {RPM}")
        plt.grid(True)
    plt.show()
    
    
    