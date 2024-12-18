import numpy as np
import pandas as pd
from Utility import *

class States:


    # Cette class permet de calculer chaque valeurs de chaque état. 
    # On crée un objet de cette classe dans laquelle on spécifie le régime et ça calcule tout automatique
    # ça enregistre dans un fichier qui correspond au régime
    # Le fichier Utility.py contient toutes les méthodes de calculs utilisées pour déterminer chaque état.
    gamma = 1.4
    Rstar = 287.058

    def __init__(self, Regime=0):
        self.Regime = Regime
        self.__regime_data()

        self.state3()
        self.state2()
        self.state1()
        self.state0()
        self.state6()
        self.state5()
        self.state4()

        self.__write_states()

    def state0(self):
        self.pt0 = self.pt2
        self.ps0 = self.pt0
        self.u0 = 0.0
        self.s0 = compute_entropy(self.T0, self.ps0)

    def state1(self):
        self.pt1 = self.pt2
        self.Tt1 = self.Tt2
        self.ps1, self.T1, self.u1 = solve_state1(self.u2, self.T2, self.ps2, self.pt2)
        self.s1 = compute_entropy(self.T1, self.ps1)

    def state2(self):
        self.T2, self.u2 = solve_state2(self.ps2, self.ps3, self.Tt2, self.T3, self.u3)
        M2_square = self.u2*self.u2/(self.gamma*self.Rstar*self.T2)
        self.pt2 = self.ps2 * (1 + (self.gamma-1)/2.0 * M2_square)**(self.gamma/(self.gamma-1))
        self.s2 = compute_entropy(self.T2, self.ps2)


    def state3(self):
        self.T3, self.u3 = solve_state3(self.Tt3, self.pt3, self.ps3)
        self.s3 = compute_entropy(self.T3, self.ps3)

    def state4(self):
        self.T4, self.u4, self.ps4 = solve_state4(self.Tt4, self.T3, self.u3, self.pt4, self.ps3, self.mdot_f, self.ps1, self.T1, self.u1)
        self.s4 = compute_entropy(self.T4, self.ps4)

    def state5(self):
        self.ps5, self.T5, self.u5 = solve_state5(self.u6, self.T6, self.ps6, self.pt6)
        self.s5 = compute_entropy(self.T5, self.ps5)

    def state6(self):
        self.pt6 = self.pt5
        self.ps6, self.T6, self.u6 = solve_state6(self.ps1, self.T1, self.u1, self.Tt6, self.pt6, self.mdot_f, self.Thrust)
        self.s6 = compute_entropy(self.T6, self.ps6)

    def get_state0(self):
        return np.array([self.ps0, self.pt0, self.T0, self.Tt0, self.u0, self.s0])     

    def get_state1(self):
        return np.array([self.ps1, self.pt1, self.T1, self.Tt1, self.u1, self.s1])     

    def get_state2(self):
        return np.array([self.ps2, self.pt2, self.T2, self.Tt2, self.u2, self.s2])    

    def get_state3(self):
        return np.array([self.ps3, self.pt3, self.T3, self.Tt3, self.u3, self.s3])     

    def get_state4(self):
        return np.array([self.ps4, self.pt4, self.T4, self.Tt4, self.u4, self.s4])        

    def get_state5(self):
        return np.array([self.ps5, self.pt5, self.T5, self.Tt5, self.u5, self.s5])        
    
    def get_state6(self):
        return np.array([self.ps6, self.pt6, self.T6, self.Tt6, self.u6, self.s6])
    



    def __write_states(self):
        header = ["State0", "State1", "State2", "State3", "State4", "State5", "State6"]
        df = pd.DataFrame(columns=header)

        df["State0"] = self.get_state0()
        df["State1"] = self.get_state1()
        df["State2"] = self.get_state2()
        df["State3"] = self.get_state3()
        df["State4"] = self.get_state4()
        df["State5"] = self.get_state5()
        df["State6"] = self.get_state6()

        line_names = ["p_s", "p_t", "T", "T_t", "u", "s"]

        df.index = line_names[:len(df)]

        filename = f"dataR/States/States_RPM{self.Regime}.csv"
        df.to_csv(filename, index=False)


    def __regime_data(self):
        df = pd.read_csv("DataMean/LabData_meanValues.csv")

        if (self.Regime == 0):
            index = 0
        elif (self.Regime == 37):
            index = 1
        elif (self.Regime == 50):
            index = 2
        elif (self.Regime == 60):
            index = 3
        elif (self.Regime == 70):
            index = 4
        elif (self.Regime == 80):
            index = 5
        elif (self.Regime == 90):
            index = 6
        elif (self.Regime == 100):
            index = 7
        

        p0 = 1e5
        self.ps2 = df['ps2'][index]*p0
        self.ps3 = df['ps3'][index]*p0
        self.pt3 = df['pt3'][index]*p0
        self.Tt3 = df['Tt3'][index]
        self.pt4 = df['pt4'][index]*p0
        self.Tt4 = df['Tt4'][index]
        self.pt5 = df['pt5'][index]*p0
        self.Tt5 = df['Tt5'][index]
        self.Tt6 = df['Tt6'][index]
        self.Thrust = df['Thrust'][index]
        self.RPM = df['RPM'][index]
        self.mdot_f = df['mdot_f'][index]*1e-3
        
        # self.Tt2 = df['Tt6'][0]
        self.T0 = df['Tt6'][0]
        self.Tt0 = self.T0
        self.Tt1 = self.T0
        self.Tt2 = self.T0

        # # Pour rendre le problème cohérent
        # self.Tt6 = self.Tt5