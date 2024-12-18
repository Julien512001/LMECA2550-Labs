import numpy as np
import pandas as pd


class Ratios:
    # On calcule tous les ratio de température et de pression

    def __init__(self, Regime = 37):
        self.Regime = Regime

        self.__read_csv()
        self.__write_ratios()

    def printRatios(self):

        tau_d, pi_d = self.get_d()
        tau_c, pi_c = self.get_c()
        tau_b, pi_b = self.get_b()
        tau_t, pi_t = self.get_t()
        tau_n, pi_n = self.get_n()

        print(f"tau_d = {tau_d}, pi_d = {pi_d}\n")
        print(f"tau_c = {tau_c}, pi_c = {pi_c}\n")
        print(f"tau_b = {tau_b}, pi_b = {pi_b}\n")
        print(f"tau_t = {tau_t}, pi_t = {pi_t}\n")
        print(f"tau_n = {tau_n}, pi_n = {pi_n}\n")

    def get_d(self):
        state_down = 2
        state_up = 1

        tau = self.Tt[state_down]/self.Tt[state_up]
        pi = self.pt[state_down]/self.pt[state_up]
        return tau, pi

    def get_c(self):
        state_down = 3
        state_up = 2

        tau = self.Tt[state_down]/self.Tt[state_up]
        pi = self.pt[state_down]/self.pt[state_up]
        return tau, pi

    def get_b(self):
        state_down = 4
        state_up = 3

        tau = self.Tt[state_down]/self.Tt[state_up]
        pi = self.pt[state_down]/self.pt[state_up]
        return tau, pi

    def get_t(self):
        state_down = 5
        state_up = 4

        tau = self.Tt[state_down]/self.Tt[state_up]
        pi = self.pt[state_down]/self.pt[state_up]
        return tau, pi

    def get_n(self):
        state_down = 6
        state_up = 5

        tau = self.Tt[state_down]/self.Tt[state_up]
        pi = self.pt[state_down]/self.pt[state_up]
        return tau, pi


    def __read_csv(self):
        filename = f"dataR/States/States_RPM{self.Regime}.csv"
        df = pd.read_csv(filename)
        
        df = np.array(df)
        
        self.ps = df[0]
        self.pt = df[1]
        self.T = df[2]
        self.Tt = df[3]
        self.u = df[4]
        # self.s = df[5]

    def __write_ratios(self):
        header = ["d", "c", "b", "t", "n"]
        df = pd.DataFrame(columns=header)

        df["d"] = self.get_d()
        df["c"] = self.get_c()
        df["b"] = self.get_b()
        df["t"] = self.get_t()
        df["n"] = self.get_n()


        filename = f"dataR/Ratios/Ratios_RPM{self.Regime}.csv"
        df.to_csv(filename, index=False)
