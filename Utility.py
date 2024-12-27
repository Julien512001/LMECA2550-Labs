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



def get_f(mdot_f, ps1, T1, u1):

    mdot_0 = ps1/(Rstar*T1)*u1*A1
    f = mdot_f/mdot_0

    return f

def compute_entropy(T, p, State, mdot_f=None, ps1=None, T1=None, u1=None):
    if State in (0, 1, 2, 3):
        cp = cpa(T)
    else:
        f = get_f(mdot_f, ps1, T1, u1)
        cp = cpg(T, f)

    return cp*np.log(T) - Rstar*np.log(p)


def area_mach_relation(M, A_A_star):
    gamma=1.4
    return (1 / M) * ((2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * M**2))**((gamma + 1) / (2 * (gamma - 1))) - A_A_star

def trouveM(A):
    A_A_star=A
    M_guess = 0.1
    M_solution, = fsolve(area_mach_relation, M_guess, args=(A_A_star,))
    return M_solution

def f_func(M):
    A = (gamma+1)/2
    B = 1 + (gamma-1)/2 *M*M
    C = (gamma+1)/(2*(gamma-1))

    return np.power(A/B, C)*M






def solve_state1(u2,T2,ps2,pt2, Tt2):

    Tt1 = Tt2
    pt1 = pt2

    M2 = u2/np.sqrt(gamma*Rstar*T2)
    Astar = A2*f_func(M2)
    M1 = trouveM(A1/Astar)

    T1 = Tt1*np.power(1+ (gamma-1)/2*M1*M1, -1)
    ps1 = pt1*np.power(Tt1/T1, -gamma/(gamma-1))
    u1 = M1*np.sqrt(gamma*Rstar*T1)

    return  ps1, T1, u1





def equations2(vars, ps2, Tt2, pt2):
    u2, T2 = vars

    eq1 = Tt2/T2 - (1 + (gamma-1)/2 * (u2*u2)/(gamma*Rstar*T2))
    eq2 = pt2/ps2 - (1 + (gamma-1)/2 * (u2*u2)/(gamma*Rstar*T2))**(gamma/(gamma-1))

    return [eq1, eq2]

def solve_state2(ps2, Tt2, pt2):
    initial_guess = [300, 500]
    sol = fsolve(equations2, initial_guess, args=(ps2, Tt2, pt2))
    u2_sol, T2_sol = sol

    return T2_sol, u2_sol





def equations3(vars, Tt3, ps3, ps2, T2, u2):
    T3, u3 = vars
    eq1 = Tt3 - (T3 + u3**2 / (2 * cpa(T3)))
    eq2 = ps2/(Rstar*T2)*u2*A2 - ps3/(Rstar*T3)*u3*A3
    return [eq1, eq2]

def solve_state3(Tt3, ps3, ps2, T2, u2):
    initial_guess = [500, 300]
    sol = fsolve(equations3, initial_guess, args=(Tt3, ps3, ps2, T2, u2))
    T3_sol, u3_sol = sol

    return T3_sol, u3_sol






def state4eq(vars, Tt4, T3, u3, ps3, ps4, mdot_f, mdot_0):
    T4, u4 = vars
    f = mdot_f/mdot_0
    eq1 = ps3/T3 * u3*A3 - ps4/T4*u4*A4 + mdot_f
    eq2 = Tt4 - (T4 + u4*u4/(2*cpg(T4,f)))
    return [eq1, eq2]
    
def solve_state4(Tt4, T3, u3, ps3, mdot_f, mdot_0):

    ps4 = ps3
    initial_guess = [500, 300]
    sol = fsolve(state4eq, initial_guess, args=(Tt4, T3, u3, ps3, ps4, mdot_f, mdot_0))
    T4_sol, u4_sol = sol
    
    T4_sol = T4_sol.item()
    u4_sol = u4_sol.item()

    return T4_sol, u4_sol








def solve_state5(u6,T6,ps6,pt6, Tt6):

    Tt5 = Tt6
    pt5 = pt6

    M6 = u6/np.sqrt(gamma*Rstar*T6)
    Astar = A6*f_func(M6)
    M5 = trouveM(A5/Astar)

    T5 = Tt5*np.power(1+ (gamma-1)/2*M5*M5, -1)
    ps5 = pt5*np.power(Tt5/T5, -gamma/(gamma-1))
    u5 = M5*np.sqrt(gamma*Rstar*T5)

    return  ps5, T5, u5


def find_T6(vars, Tt6, T, ps6):
    T6, u6, mdot_6 = vars

    eq1 = Tt6/T6 - (1 + (gamma-1)/2 * u6*u6/(gamma*Rstar*T6))
    eq2 = T - mdot_6*u6
    eq3 = mdot_6 - ps6/(Rstar*T6)*u6*A6
    return [eq1, eq2, eq3]

def solve_state6(Tt6, Thrust, ps6):

    initial_guess = [400, 300, 1.0]
    T6, u6, mdot_6 = fsolve(find_T6, initial_guess, args=(Tt6, Thrust, ps6))

    T6 = T6.item()
    u6 = u6.item()


    print(f"mdot_6 = {mdot_6}")

    return T6, u6