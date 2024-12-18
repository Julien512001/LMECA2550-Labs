import numpy as np
from scipy.optimize import fsolve

gamma = 1.4
Rstar = 287.058

A1 = 5.168e-3
A2 = 2.818e-3
A3 = 4.112e-3
A4 = 6.323e-3
A5 = 3.519e-3
A6 = 3.318e-3

def cpa(T):
    if 200 < T <= 800:
        return 1.0189e3 - 0.137847*T + 1.9843e-4*T**2 + 4.2399e-7*T**3 - 3.7632e-10*T**4
    elif 800 < T <= 2200:
        return 7.9865e2 + 0.5339*T - 2.2882e-4*T**2 + 3.7421e-8*T**3
    else:
        raise ValueError("Temperature out of bounds for Cpa calculation.")

def Bt(T):

    if 200 < T <= 800:
        return -3.59494e2 + 4.5164*T + 2.8116e-3*T**2 - 2.1709e-5*T**3 + 2.8689e-8*T**4 - 1.2263e-11*T**5
    elif 800 < T <= 2200:
        return 1.0888e3 - 0.1416*T + 1.916e-3*T**2 - 1.2401e-6*T**3 + 3.0669e-10*T**4 - 2.6117e-14*T**5
    else:
        raise ValueError("Temperature out of bounds for Bt calculation.")

def cpg(T, f):
    if f <= 0:
        raise ValueError("The fuel-to-air ratio f must be positive.")
    return cpa(T) + Bt(T) * (f) / (f+1)

def equations2(vars, ps2, ps3, Tt2, T3, u3):
    u2, T2 = vars

    eq1 = ps2 * (u2 / (Rstar * T2)) * A2 - ps3 * (u3 / (Rstar * T3)) * A3
    # eq2 = Tt2 / T2 - (1 + ((gamma - 1) / (2 * gamma)) * (u2**2) / (Rstar * T2))
    eq2 = Tt2 - T2 - (u2**2) / (2 * cpa(T2))

    return [eq1, eq2]

def area_mach_relation(M, A_A_star):
    gamma=1.4
    return (1 / M) * ((2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * M**2))**((gamma + 1) / (2 * (gamma - 1))) - A_A_star

def trouveM(A):
    A_A_star=A
    M_guess = 0.1
    M_solution, = fsolve(area_mach_relation, M_guess, args=(A_A_star,))
    return M_solution

def state3eq(vars, Tt3, pt3, ps3):
    T3, u3 = vars
    eq1 = Tt3 - (T3 + u3**2 / (2 * cpa(T3)))
    eq2 = pt3 - ps3 * (1 + u3**2 / (2 * Rstar * T3))**(gamma / (gamma - 1))
    return [eq1, eq2]

def state4eq(vars, Tt4, T3, u3, ps3, pt4, mdot_f, mdot_0):
    T4, u4, ps4 = vars
    f = mdot_f/mdot_0
    eq1 = ps3/T3 * u3*A3 - ps4/T4*u4*A4 + mdot_f
    eq2 = T4 - (Tt4 - u4/(2*cpg(T4,f)))
    eq3 = pt4 - ps4 * (1 + 1/(Rstar*T4)*u4*u4/2)
    return [eq1, eq2, eq3]


def solve_state1(u2,T2,ps2,pt2):
    # Étape 1 : Calcul de M2 (Mach en sortie)
    M2 = u2 / np.sqrt(gamma * Rstar * T2)
    Astar  = A2 / (((gamma + 1) / 2)**(-(gamma + 1) / (2 * (gamma - 1))) * 
                   (1 + (gamma - 1) / 2 * M2**2)**((gamma + 1) / (2 * (gamma - 1))) / M2)
    # Étape 2 : Calcul du rapport d'aire A1/A2 et M1
    A_ratio = A1/Astar
    
    M1 = trouveM(A_ratio)

    # Étape 3 : Utiliser les relations isentropiques pour trouver les autres paramètres à l'entrée
    T1 = T2 * (1 + (gamma - 1) / 2 * M1**2) / (1 + (gamma - 1) / 2 * M2**2)

    ps1 = ps2 * (1 + (gamma - 1) / 2 * M1**2)**(-gamma / (gamma - 1)) / (1 + (gamma - 1) / 2 * M2**2)**(-gamma / (gamma - 1))
    
    pt1 = pt2  # Conservation de la pression totale dans un écoulement isentropique
    u1 = M1 * np.sqrt(gamma * Rstar * T1)
    Tt1 = T1 * (1 + (gamma - 1) / 2 * M1**2)

    return  ps1, T1, u1

def solve_state2(ps2, ps3, Tt2, T3, u3):
    initial_guess = [300, 500]
    sol = fsolve(equations2, initial_guess, args=(ps2, ps3, Tt2, T3, u3))
    u2_sol, T2_sol = sol

    return T2_sol, u2_sol


def solve_state3(Tt3, pt3, ps3):
    initial_guess = [500, 300]  # Estimations initiales pour T3 (K) et u3 (m/s)
    sol = fsolve(state3eq, initial_guess, args=(Tt3, pt3, ps3))
    T3_sol, u3_sol = sol

    return T3_sol, u3_sol

def solve_state4(Tt4, T3, u3, pt4, ps3, mdot_f, ps1, T1, u1, simplified=True):
    mdot_0 = ps1/(Rstar*T1)*u1*A1

    initial_guess = [500, 300, 100000]
    sol = fsolve(state4eq, initial_guess, args=(Tt4, T3, u3, ps3, pt4, mdot_f, mdot_0))
    T4_sol, u4_sol, ps4_sol = sol
    
    T4_sol = T4_sol.item()
    u4_sol = u4_sol.item()
    ps4_sol = ps4_sol.item()
    return T4_sol, u4_sol, ps4_sol

def solve_state5(u6,T6,ps6,pt6):
    # Étape 1 : Calcul de M2 (Mach en sortie)
    M6 = u6 / np.sqrt(gamma * Rstar * T6)
    Astar  = A6 / (((gamma + 1) / 2)**(-(gamma + 1) / (2 * (gamma - 1))) * 
                   (1 + (gamma - 1) / 2 * M6**2)**((gamma + 1) / (2 * (gamma - 1))) / M6)
    # Étape 2 : Calcul du rapport d'aire A1/A2 et M1
    A_ratio = A1/Astar
    
    M5 = trouveM(A_ratio)

    # Étape 3 : Utiliser les relations isentropiques pour trouver les autres paramètres à l'entrée
    T5 = T6 * (1 + (gamma - 1) / 2 * M5**2) / (1 + (gamma - 1) / 2 * M6**2)

    ps5 = ps6 * (1 + (gamma - 1) / 2 * M5**2)**(-gamma / (gamma - 1)) / (1 + (gamma - 1) / 2 * M6**2)**(-gamma / (gamma - 1))
    
    pt5 = pt6  # Conservation de la pression totale dans un écoulement isentropique
    u5 = M5 * np.sqrt(gamma * Rstar * T5)
    Tt5 = T5 * (1 + (gamma - 1) / 2 * M5**2)
    ps5 = ps5.item()

    T5 = T5.item()
    u5 = u5.item()
    return  ps5, T5, u5


def find_T6(T6, Tt6, u6, f):
    # Quelle équation utiliser ???

    # eq1 = T6 - (Tt6 - u6*u6/(2*cpg(T6, f)))
    eq1 = Tt6/T6 - (1+ (gamma-1)/2 * u6*u6/(gamma*Rstar*T6))
    return eq1

def solve_state6(ps1, T1, u1, Tt6, pt6, mdot_f, Thrust):
    mdot_0 = ps1/(Rstar*T1)*u1*A1
    mdot_e = mdot_0 + mdot_f
    u6 = Thrust/mdot_e
    
    f = mdot_f/mdot_0

    initial_guess = 400
    T6 = fsolve(find_T6, initial_guess, args=(Tt6, u6, f))

    ps6 = pt6*(Tt6/T6)**(-gamma/(gamma-1))

    ps6 = ps6.item()
    T6 = T6.item()
    u6 = u6.item()
    
    return ps6, T6, u6