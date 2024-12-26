import numpy as np
import pandas as pd



class Parameters:

    def __init__(self):

        self.data = self.__readCSV().T
        self.__writeCSV()
    
    def __readCSV(self):

        df = pd.read_csv("DataMean/Labo_Result_2024_12_13_14_08SaveButton.txt", sep="\t")

        ps2 = df.iloc[:,4].to_numpy()
        ps3 = df.iloc[:,5].to_numpy()
        pt3 = df.iloc[:,6].to_numpy()
        pt4 = df.iloc[:,7].to_numpy()
        pt5 = df.iloc[:,8].to_numpy()
        Tt3 = df.iloc[:,9].to_numpy() + 273.15
        Tt4 = df.iloc[:,10].to_numpy() + 273.15
        Tt5 = df.iloc[:,11].to_numpy() + 273.15

        Tt6 = df.iloc[:,13].to_numpy() + 273.15

        Thrust = df.iloc[:,15].to_numpy()
        # Thrust = Thrust - np.abs(Thrust[0])

        RPM = df.iloc[:,16].to_numpy()
        
        mdot_f = df.iloc[:,20].to_numpy()
        mdot_f = mdot_f + np.abs(mdot_f[0])



        return np.array([ps2, ps3, pt3, pt4, pt5, Tt3, Tt4, Tt5, Tt6, Thrust, RPM, mdot_f])

    def __writeCSV(self):
        v0 = self.RPM_0()
        v1 = self.RPM_37()
        v2 = self.RPM_50()
        v3 = self.RPM_60()
        v4 = self.RPM_70()
        v5 = self.RPM_80()
        v6 = self.RPM_90()
        v7 = self.RPM_100()



        df = pd.DataFrame([v0, v1, v2, v3, v4,
                       v5, v6, v7])

        header = ["ps2", "ps3", "pt3", "pt4", "pt5", "Tt3", "Tt4", "Tt5", "Tt6", "Thrust", "RPM", "mdot_f"]
        df.to_csv('DataMean/LabData_meanValues.csv', index=False, header=header)

    def RPM_0(self):
        lowIndex = 0
        highIndex = 4

        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_37(self):
        lowIndex = 5
        highIndex = 29

        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_50(self):
        lowIndex = 30
        highIndex = 44

        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_60(self):
        lowIndex = 45
        highIndex = 59

        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_70(self):
        lowIndex = 60
        highIndex = 74

        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_80(self):
        lowIndex = 75
        highIndex = 89


        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_90(self):
        lowIndex = 90
        highIndex = 99


        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    def RPM_100(self):
        lowIndex = 100
        highIndex = 119


        newData = np.zeros(self.data.shape[1])

        for i in range(len(newData)):
            newData[i] = np.mean(self.data[lowIndex:highIndex, i])

        return newData
    
    