import math
import numpy as np
import pandas as pd
import streamlit as st


# pre assumed referednce conditon
R = 8.31446261815324
tempref = 298.15
pressref = 101325.0


# the parameter data tc pc and all

all_para_dat = {
    "Methane":(16.043, 0.012, 190.6, 45.99, 0.286, 98.6, 111.4),
    "Ethane":(30.070, 0.100, 305.3, 48.72, 0.279, 145.5, 184.6),
    "Propane": (44.097,0.152,369.8,42.48, 0.276, 200.0, 231.1),
    "n-Butane": (58.123, 0.200, 425.1,37.96,0.274, 255.0, 272.7),
    "n-Pentane":(72.150, 0.252, 469.7, 33.70, 0.270, 313.0, 309.2),
    "n-Hexane":(86.177,0.301, 507.6, 30.25, 0.266, 371.0, 341.9),
    "n-Heptane":(100.204,0.350, 540.2, 27.40, 0.261, 428.0, 371.6),
    "n-Octane": (114.231,0.400,568.7, 24.90, 0.256, 486.0, 398.8),
    "n-Nonane":(128.258,0.444,594.6, 22.90, 0.252, 544.0, 424.0),
    "n-Decane":(142.285,0.492,617.7, 21.10, 0.247, 600.0, 447.3),
    "Isobutane": (58.123, 0.181, 408.1,36.48,0.282,262.7, 261.4),
    "Isooctane":(114.231, 0.302, 544.0, 25.68, 0.266,468.0, 372.4),
    "Cyclopentane": (70.134, 0.196, 511.8, 45.02,0.273, 258.0, 322.4),
    "Cyclohexane": (84.161, 0.210, 553.6, 40.73,0.273, 308.0, 353.9),
    "Methylcyclopentane": (84.161, 0.230, 532.8,37.85, 0.272, 319.0, 345.0),
    "Methylcyclohexane": (98.188, 0.235, 572.2,34.71, 0.269, 368.0, 374.1),
    "Ethylene": (28.054, 0.087, 282.3, 50.40,0.281, 131.0, 169.4),
    "Propylene": (42.081, 0.140, 365.6,46.65, 0.289, 188.4, 225.5),
    "1-Butene": (56.108, 0.191, 420.0,40.43, 0.277, 239.3, 266.9),
    "cis-2-Butene": (56.108, 0.205,435.6, 42.43, 0.273, 233.8, 276.9),
    "trans-2-Butene": (56.108,0.218, 428.6, 41.00, 0.275, 237.7, 274.0),
    "1-Hexene": (84.161, 0.280, 504.0,31.40, 0.265, 354.0, 336.3),
    "Isobutylene": (56.108, 0.194, 417.9, 40.00, 0.275, 238.9, 266.3),
    "1,3-Butadiene": (54.092, 0.190,425.2, 42.77, 0.267, 220.4, 268.7),
    "Cyclohexene":(82.145, 0.212, 560.4, 43.50, 0.272, 291.0, 356.1),
    "Acetylene": (26.038, 0.187, 308.3,61.39, 0.271, 113.0, 189.4),
    "Benzene": (78.114, 0.210, 562.2, 48.98, 0.271, 259.0, 353.2),
    "Toluene":(92.141, 0.262, 591.8, 41.06,0.264, 316.0, 383.8),
    "Ethylbenzene": (106.167, 0.303, 617.2, 36.06, 0.263, 374.0, 409.4),
    "Cumene": (120.194, 0.326, 631.1, 32.09, 0.261, 427.0, 425.6),
    "o-Xylene": (106.167, 0.310, 630.3, 37.34, 0.263, 369.0, 417.6),
    "m-Xylene": (106.167, 0.326, 617.1, 35.36, 0.259, 376.0, 412.3),
    "p-Xylene": (106.167, 0.322, 616.2, 35.11, 0.260, 379.0, 411.5),
    "Styrene": (104.152, 0.297, 636.0, 38.40, 0.256, 352.0, 418.3),
    "Naphthalene": (128.174, 0.302, 748.4, 40.51, 0.269, 413.0, 491.2),
    "Biphenyl": (154.211, 0.365, 789.3, 38.50, 0.295, 502.0, 528.2),
    "Formaldehyde": (30.026, 0.282, 408.0, 65.90, 0.223, 115.0, 254.1),
    "Acetaldehyde": (44.053, 0.291, 466.0, 55.50, 0.221, 154.0, 294.0),
    "Methyl acetate": (74.079, 0.331, 506.6, 47.50, 0.257, 228.0, 330.1),
    "Ethyl acetate": (88.106, 0.366, 523.3, 38.80, 0.255, 286.0, 350.2),
    "Acetone": (58.080, 0.307, 508.2, 47.01, 0.233, 209.0, 329.4),
    "Methyl ethyl ketone": (72.107, 0.323, 535.5, 41.50, 0.249, 267.0, 352.8),
    "Diethyl ether": (74.123, 0.281, 466.7, 36.40, 0.263, 280.0, 307.6),
    "Methyl t-butyl ether": (88.150, 0.266, 497.1, 34.30, 0.273, 329.0, 328.4),
    "Methanol": (32.042, 0.564, 512.6, 80.97, 0.224, 118.0, 337.9),
    "Ethanol": (46.069, 0.645, 513.9, 61.48, 0.240, 167.0, 351.4),
    "1-Propanol": (60.096, 0.622, 536.8, 51.75, 0.254, 219.0, 370.4),
    "1-Butanol": (74.123, 0.594, 563.1, 44.23, 0.260, 275.0, 390.8),
    "1-Hexanol": (102.177, 0.579, 611.4, 35.10, 0.263, 381.0, 430.6),
    "2-Propanol": (60.096, 0.668, 508.3, 47.62, 0.248, 220.0, 355.4),
    "Phenol": (94.113, 0.444, 694.3, 61.30, 0.243, 229.0, 455.0),
    "Ethylene glycol": (62.068, 0.487, 719.7, 77.00, 0.246, 191.0, 470.5),
    "Acetic acid": (60.053, 0.467, 592.0, 57.86, 0.211, 179.7, 391.1),
    "n-Butyric acid": (88.106, 0.681, 615.7, 40.64, 0.232, 291.7, 436.4),
    "Benzoic acid": (122.123, 0.603, 751.0, 44.70, 0.246, 344.0, 522.4),
    "Acetonitrile": (41.053, 0.338, 545.5, 48.30, 0.184, 173.0, 354.8),
    "Methylamine": (31.057, 0.281, 430.1, 74.60, 0.321, 154.0, 266.8),
    "Ethylamine": (45.084, 0.285, 456.2, 56.20, 0.307, 207.0, 289.7),
    "Nitromethane": (61.040, 0.348, 588.2, 63.10, 0.223, 173.0, 374.4),
    "Carbon tetrachloride": (153.822, 0.193, 556.4, 45.60, 0.272, 276.0, 349.8),
    "Chloroform": (119.377, 0.222, 536.4, 54.72, 0.293, 239.0, 334.3),
    "Dichloromethane": (84.932, 0.199, 510.0, 60.80, 0.265, 185.0, 312.9),
    "Methyl chloride": (50.488, 0.153, 416.3, 66.80, 0.276, 143.0, 249.1),
    "Ethyl chloride": (64.514, 0.190, 460.4, 52.70, 0.275, 200.0, 285.4),
    "Chlorobenzene": (112.558, 0.250, 632.4, 45.20, 0.265, 308.0, 404.9),
    "Tetrafluoroethane": (102.030, 0.327, 374.2, 40.60, 0.258, 198.0, 247.1),
    "Argon": (39.948, 0.000, 150.9, 48.98, 0.291, 74.6, 87.3),
    "Krypton": (83.800, 0.000, 209.4, 55.02, 0.288, 91.2, 119.8),
    "Xenon": (131.30, 0.000, 289.7, 58.40, 0.286, 118.0, 165.0),
    "Helium": (4.003, -0.390, 5.2, 2.28, 0.302, 57.3, 4.2),
    "Hydrogen": (2.016, -0.216, 33.19, 13.13, 0.305, 64.1, 20.4),
    "Oxygen": (31.999, 0.022, 154.6, 50.43, 0.288, 73.4, 90.2),
    "Nitrogen": (28.014, 0.038, 126.2, 34.00, 0.289, 89.2, 77.3),
    "Air": (28.851, 0.035, 132.2, 37.45, 0.289, 84.8, None),
    "Chlorine": (70.905, 0.069, 417.2, 77.10, 0.265, 124.0, 239.1),
    "Carbon monoxide": (28.010, 0.048, 132.9, 34.99, 0.299, 93.4, 81.7),
    "Carbon dioxide": (44.010, 0.224, 304.2, 73.83, 0.274, 94.0, None),
    "Carbon disulfide": (76.143, 0.111, 552.0, 79.00, 0.275, 160.0, 319.4),
    "Hydrogen sulfide": (34.082, 0.094, 373.5, 89.63, 0.284, 98.5, 212.8),
    "Sulfur dioxide": (64.065, 0.245, 430.8, 78.84, 0.269, 122.0, 263.1),
    "Sulfur trioxide": (80.064, 0.424, 490.9, 82.10, 0.255, 127.0, 317.9),
    "Nitric oxide (NO)": (30.006, 0.583, 180.2, 64.80, 0.251, 58.0, 121.4),
    "Nitrous oxide (N2O)": (44.013, 0.141, 309.6, 72.45, 0.274, 97.4, 184.7),
    "Hydrogen chloride": (36.461, 0.132, 324.7, 83.10, 0.249, 81.0, 188.2),
    "Hydrogen cyanide": (27.026, 0.410, 456.7, 53.90, 0.197, 139.0, 298.9),
    "Water": (18.015, 0.345, 647.1, 220.55, 0.229, 55.9, 373.2),
    "Ammonia": (17.031, 0.253, 405.7, 112.80, 0.242, 72.5, 239.7),
    "Nitric acid": (63.013, 0.714, 520.0, 68.90, 0.231, 145.0, 356.2)
}


def load_database():
    datbase = {}
    for name, values in all_para_dat.items():
        MW, omega, Tc, Pc_bar, Zc, Vc_cm3, Tb = values
        datbase[name] = {
            "MW": MW,
            "omega": omega,
            "Tc": Tc,
            "Pc": Pc_bar * 100000.0,
            "Pc_bar": Pc_bar,
            "Zc": Zc,
            "Vc": Vc_cm3 * 1e-6,
            "Vc_cm3": Vc_cm3,
            "Tb": Tb
        }

    return datbase


def search_compound(srchtst, datbse):
    srchtst = srchtst.strip().lower()

    if not srchtst:
        return list(datbse.keys())

    return [
        nm for nm in datbse
        if srchtst in nm.lower()
    ]


def get_critical_properties(materal, database):
    if materal not in database:
        raise ValueError("Compound not found.")

    return database[materal]



def get_eos_parameters(esnm):

    pramt = {
        "van der Waals": {
            "Omega": 27 / 64,
            "Psi": 1 / 8,
            "epsilon": 0.0,
            "sigma": 0.0
        },

        "Redlich-Kwong": {
            "Omega": 0.42748,
            "Psi": 0.08664,
            "epsilon": 1.0,
            "sigma": 0.0
        },

        "Soave-Redlich-Kwong": {
            "Omega": 0.42747,
            "Psi": 0.08664,
            "epsilon": 1.0,
            "sigma": 0.0
        },

        "Peng-Robinson": {
            "Omega": 0.45724,
            "Psi": 0.07780,
            "epsilon": 1 + math.sqrt(2),
            "sigma": 1 - math.sqrt(2)
        }
    }

    return pramt[esnm]


def calculate_alpha(T, Tc, omega, eos_name):

    Tr = T / Tc

    if eos_name == "van der Waals":
        return 1.0

    elif eos_name == "Redlich-Kwong":
        return Tr ** -0.5

    elif eos_name == "Soave-Redlich-Kwong":
        m = 0.480 + 1.574 * omega - 0.176 * omega ** 2
        return (1 + m * (1 - math.sqrt(Tr))) ** 2

    elif eos_name == "Peng-Robinson":
        m = 0.37464 + 1.54226 * omega - 0.26992 * omega ** 2
        return (1 + m * (1 - math.sqrt(Tr))) ** 2

    raise ValueError("Unknown EOS model.")


def calculate_a(T, Tc, Pc, omega, eos_name):

    parmt = get_eos_parameters(eos_name)

    alp = calculate_alpha(T, Tc, omega, eos_name)

    a = (
        parmt["Omega"]
        * R ** 2
        * Tc ** 2
        / Pc
        * alp
    )

    return a


def calcb(Tc, Pc, esman):

    prmt = get_eos_parameters(esman)

    b = prmt["Psi"] * R * Tc / Pc

    return b


def calculate_da_dT(T, Tc, Pc, omega, eos_name):

    step = max(1e-4, T * 1e-5)

    low_T = max(T - step, 1e-8)
    high_T = T + step

    return (
        calculate_a(high_T, Tc, Pc, omega, eos_name)
        - calculate_a(low_T, Tc, Pc, omega, eos_name)
    ) / (high_T - low_T)


def calculate_AB(P, T, a, b):

    A = a * P / (R ** 2 * T ** 2)
    B = b * P / (R * T)

    return A, B


def get_cubic_coefficients(A, B, epsilon, sigma):

    u = epsilon + sigma
    w = epsilon * sigma

    c2 = (u - 1) * B - 1

    c1 = A + w * B ** 2 - u * B * (1 + B)

    c0 = -A * B - w * B ** 2 * (1 + B)

    return [1, c2, c1, c0]


def solve_cubic(coefficients):

    roots = np.roots(coefficients)

    real_roots = []

    for root in roots:

        if abs(root.imag) < 1e-8 and root.real > 0:
            real_roots.append(float(root.real))

    return sorted(real_roots)


def calculate_ln_phi(Z, A, B, epsilon, sigma):

    if Z <= B:
        raise ValueError("Invalid compressibility root.")

    ln_phi = Z - 1 - math.log(Z - B)

    if abs(epsilon - sigma) < 1e-12:
        ln_phi -= A / Z

    else:

        ratio = (Z + epsilon * B) / (Z + sigma * B)

        if ratio <= 0:
            raise ValueError("Invalid fugacity logarithm.")

        ln_phi -= (
            A / (B * (epsilon - sigma))
        ) * math.log(ratio)

    return ln_phi


def calculate_compressibility(P, T, properties, eos_name, phase):

    Tc = properties["Tc"]
    Pc = properties["Pc"]
    omega = properties["omega"]

    if P <= 0 or T <= 0:
        raise ValueError("Pressure and temperature must be positive.")

    a = calculate_a(T, Tc, Pc, omega, eos_name)

    b = calcb(Tc, Pc, eos_name)

    parameters = get_eos_parameters(eos_name)

    A, B = calculate_AB(P, T, a, b)

    coefficients = get_cubic_coefficients(
        A,
        B,
        parameters["epsilon"],
        parameters["sigma"]
    )

    roots = solve_cubic(coefficients)

    if not roots:
        raise ValueError("No positive real root found.")

    if phase == "Liquid":
        Z = roots[0]
    else:
        Z = roots[-1]

    V = Z * R * T / P

    ln_phi = calculate_ln_phi(
        Z,
        A,
        B,
        parameters["epsilon"],
        parameters["sigma"]
    )

    phi = math.exp(ln_phi)

    fugacity = phi * P

    return {
        "Z": Z,
        "V": V,
        "a": a,
        "b": b,
        "A": A,
        "B": B,
        "roots": roots,
        "ln_phi": ln_phi,
        "phi": phi,
        "fugacity": fugacity
    }


# ============================================================
# Pressure, volume, and compressibility calculations
# ============================================================

def calculate_pressure(T, V, properties, eos_name):

    if T <= 0 or V <= 0:
        raise ValueError("Temperature and volume must be positive.")

    Tc = properties["Tc"]
    Pc = properties["Pc"]
    omega = properties["omega"]

    a = calculate_a(T, Tc, Pc, omega, eos_name)

    b = calcb(Tc, Pc, eos_name)

    parameters = get_eos_parameters(eos_name)

    if V <= b:
        raise ValueError("Volume must be greater than b.")

    denominator = (
        (V + parameters["epsilon"] * b)
        * (V + parameters["sigma"] * b)
    )

    if abs(denominator) < 1e-30:
        raise ValueError("Invalid EOS denominator.")

    P = (
        R * T / (V - b)
        - a / denominator
    )

    return P


def calculate_volume(P, T, properties, eos_name, phase):

    result = calculate_compressibility(
        P, T, properties, eos_name, phase
    )

    return result["V"]


def calculate_z(P, V, T):

    return P * V / (R * T)


def calculate_cp(T, A, B, C, D):

    return R * (A + B*T + C*T**2 + D/(T**2))


def calculate_ideal_enthalpy(
    T, Tref, A, B, C, D, Href=0.0
):

    H = Href + R * (
        A * (T - Tref)
        + B / 2 * (T**2 - Tref**2)
        + C / 3 * (T**3 - Tref**3)
        + D * (1 / Tref - 1 / T)
    )

    return H


def calculate_ideal_entropy(
    T, Tref, P, Pref, A, B, C, D, Sref=0.0
):

    if T <= 0 or Tref <= 0 or P <= 0 or Pref <= 0:
        raise ValueError("Temperature and pressure must be positive.")

    thermal_entropy = R * (
        A * math.log(T / Tref)
        + B * (T - Tref)
        + C / 2 * (T**2 - Tref**2)
        + D / 2 * (1 / Tref**2 - 1 / T**2)
    )

    pressure_entropy = -R * math.log(P / Pref)

    return Sref + thermal_entropy + pressure_entropy



cp_table_raw = {
    # Each row stores A and the table values for 10³B, 10⁶C, and 10⁻⁵D.
    "Methane": (1.702, 9.081, -2.164, 0.0),
    "Ethane": (1.131, 19.225, -5.561, 0.0),
    "Propane": (1.213, 28.785, -8.824, 0.0),
    "n-Butane": (1.935, 36.915, -11.402, 0.0),
    "iso-Butane": (1.677, 37.853, -11.945, 0.0),
    "n-Pentane": (2.464, 45.351, -14.111, 0.0),
    "n-Hexane": (3.025, 53.722, -16.791, 0.0),
    "n-Heptane": (3.570, 62.127, -19.486, 0.0),
    "n-Octane": (4.108, 70.567, -22.208, 0.0),
    "Ethylene": (1.424, 14.394, -4.392, 0.0),
    "Propylene": (1.637, 22.706, -6.915, 0.0),
    "1-Butene": (1.967, 31.630, -9.873, 0.0),
    "1-Pentene": (2.691, 39.753, -12.447, 0.0),
    "1-Hexene": (3.220, 48.189, -15.157, 0.0),
    "1-Heptene": (3.768, 56.588, -17.847, 0.0),
    "1-Octene": (4.324, 64.960, -20.521, 0.0),
    "Acetaldehyde": (1.693, 17.978, -6.158, 0.0),
    "Acetylene": (6.132, 1.952, 0.0, -1.299),
    "Benzene": (-0.206, 39.064, -13.301, 0.0),
    "1,3-Butadiene": (2.734, 26.786, -8.882, 0.0),
    "Cyclohexane": (-3.876, 63.249, -20.928, 0.0),
    "Ethanol": (3.518, 20.001, -6.002, 0.0),
    "Ethylbenzene": (1.124, 55.380, -18.476, 0.0),
    "Ethylene oxide": (-0.385, 23.463, -9.296, 0.0),
    "Formaldehyde": (2.264, 7.022, -1.877, 0.0),
    "Methanol": (2.211, 12.216, -3.450, 0.0),
    "Styrene": (2.050, 50.192, -16.662, 0.0),
    "Toluene": (0.290, 47.052, -15.716, 0.0),
    "Air": (3.355, 0.575, 0.0, -0.016),
    "Ammonia": (3.578, 3.020, 0.0, -0.186),
    "Bromine": (4.493, 0.056, 0.0, -0.154),
    "Carbon monoxide": (3.376, 0.557, 0.0, -0.031),
    "Carbon dioxide": (5.457, 1.045, 0.0, -1.157),
    "Carbon disulfide": (6.311, 0.805, 0.0, -0.906),
    "Chlorine": (4.442, 0.089, 0.0, -0.344),
    "Hydrogen": (3.249, 0.422, 0.0, 0.083),
    "Hydrogen sulfide": (3.931, 1.490, 0.0, -0.232),
    "Hydrogen chloride": (3.156, 0.623, 0.0, 0.151),
    "Hydrogen cyanide": (4.736, 1.359, 0.0, -0.725),
    "Nitrogen": (3.280, 0.593, 0.0, 0.040),
    "Nitrous oxide": (5.328, 1.214, 0.0, -0.928),
    "Nitric oxide": (3.387, 0.629, 0.0, 0.014),
    "Nitrogen dioxide": (4.982, 4.195, 0.0, -0.792),
    "Dinitrogen tetroxide": (11.660, 2.257, 0.0, -2.787),
    "Oxygen": (3.639, 0.506, 0.0, -0.227),
    "Sulfur dioxide": (5.699, 0.801, 0.0, -1.015),
    "Sulfur trioxide": (8.060, 1.056, 0.0, -2.028),
    "Water": (3.470, 1.450, 0.0, 0.121),
}

cp_database = {
    name: (A, B * 1e-3, C * 1e-6, D * 1e5)
    for name, (A, B, C, D) in cp_table_raw.items()
}


def calculate_residual_properties(T, P, properties, eos_name, Z):

    Tc = properties["Tc"]
    Pc = properties["Pc"]
    omega = properties["omega"]

    a = calculate_a(T, Tc, Pc, omega, eos_name)

    da_dT = calculate_da_dT(
        T, Tc, Pc, omega, eos_name
    )

    b = calcb(Tc, Pc, eos_name)

    parameters = get_eos_parameters(eos_name)

    A, B = calculate_AB(P, T, a, b)

    if Z <= B:
        raise ValueError("Invalid Z for residual properties.")

    epsilon = parameters["epsilon"]
    sigma = parameters["sigma"]

    if abs(epsilon - sigma) < 1e-12:

        V = Z * R * T / P

        log_term = b / V

    else:

        ratio = (
            (Z + epsilon * B)
            / (Z + sigma * B)
        )

        if ratio <= 0:
            raise ValueError("Invalid residual-property logarithm.")

        log_term = (
            math.log(ratio)
            / (epsilon - sigma)
        )

    H_res = (
        R * T * (Z - 1)
        + (T * da_dT - a) / b * log_term
    )

    S_res = (
        R * math.log(Z - B)
        + da_dT / b * log_term
    )

    return H_res, S_res


def calculate_enthalpy_entropy(
    T, P, properties, eos_name, Z,
    cp_A, cp_B, cp_C, cp_D,
    Tref, Pref, Href, Sref
):

    H_ideal = calculate_ideal_enthalpy(
        T, Tref,
        cp_A, cp_B, cp_C, cp_D,
        Href
    )

    S_ideal = calculate_ideal_entropy(
        T, Tref, P, Pref,
        cp_A, cp_B, cp_C, cp_D,
        Sref
    )

    H_res, S_res = calculate_residual_properties(
        T, P, properties, eos_name, Z
    )

    return {
        "H_ideal": H_ideal,
        "S_ideal": S_ideal,
        "H_res": H_res,
        "S_res": S_res,
        "H": H_ideal + H_res,
        "S": S_ideal + S_res
    }



def make_pv_plot(T, properties, eos_names):

    fig = go.Figure()

    for eos_name in eos_names:

        b = calcb(
            properties["Tc"],
            properties["Pc"],
            eos_name
        )

        Vmin = max(b * 1.03, 1e-7)

        Vmax = max(
            Vmin * 1.2,
            12 * R * T / properties["Pc"]
        )

        volumes = np.geomspace(Vmin, Vmax, 250)

        valid_volumes = []
        pressures = []

        for V in volumes:

            try:

                P = calculate_pressure(
                    T, V, properties, eos_name
                )

                if P > 0 and np.isfinite(P):

                    valid_volumes.append(V)
                    pressures.append(P / 1e5)

            except (ValueError, ZeroDivisionError, OverflowError):
                continue

        if pressures:

            fig.add_trace(
                go.Scatter(
                    x=valid_volumes,
                    y=pressures,
                    mode="lines",
                    name=eos_name
                )
            )

    fig.update_layout(
        title=f"Pressure vs Molar Volume at {T:.2f} K",
        xaxis_title="Molar Volume (m³/mol)",
        yaxis_title="Pressure (bar)",
        template="plotly_white"
    )

    return fig


def make_z_pressure_plot(
    T, properties, eos_names, phase
):

    fig = go.Figure()

    pressures_bar = np.geomspace(0.1, 100, 100)

    for eos_name in eos_names:

        z_values = []
        valid_pressures = []

        for P_bar in pressures_bar:

            try:

                result = calculate_compressibility(
                    P_bar * 1e5,
                    T,
                    properties,
                    eos_name,
                    phase
                )

                z_values.append(result["Z"])
                valid_pressures.append(P_bar)

            except (ValueError, OverflowError):
                continue

        if z_values:

            fig.add_trace(
                go.Scatter(
                    x=valid_pressures,
                    y=z_values,
                    mode="lines",
                    name=eos_name
                )
            )

    fig.update_layout(
        title=f"Compressibility Factor vs Pressure at {T:.2f} K",
        xaxis_title="Pressure (bar)",
        yaxis_title="Compressibility Factor (Z)",
        xaxis_type="log",
        template="plotly_white"
    )

    return fig


def show_compound_selector(database):

    st.subheader("Choose a compound")

    search_text = st.text_input(
        "Find a compound",
        placeholder="Try methane, benzene, ethanol, or water"
    )

    matches = search_compound(search_text, database)

    if not matches:

        st.warning("No compound with that name came up.")

        return None, None

    selected_name = st.selectbox(
        f"Choose a compound ({len(matches)} matches)",
        matches
    )

    properties = get_critical_properties(
        selected_name,
        database
    )

    st.success(f"Using {selected_name}")

    st.markdown("#### Critical Properties")

    property_table = pd.DataFrame({
        "Property": [
            "Molecular Weight",
            "Acentric Factor",
            "Critical Temperature",
            "Critical Pressure",
            "Critical Compressibility",
            "Critical Volume",
            "Normal Boiling Temperature"
        ],

        "Value": [
            f'{properties["MW"]} g/mol',
            properties["omega"],
            f'{properties["Tc"]} K',
            f'{properties["Pc_bar"]} bar',
            properties["Zc"],
            f'{properties["Vc_cm3"]} cm³/mol',
            (
                "Not available"
                if properties["Tb"] is None
                else f'{properties["Tb"]} K'
            )
        ]
    })

    st.dataframe(
        property_table,
        hide_index=True,
        use_container_width=True
    )

    return selected_name, properties



def main():
    st.set_page_config(page_title="Real Gas PVT", page_icon="🧪", layout="centered")

    

    st.title("Jyoti's PVT calculator")
    st.write("Choose a compound and set the operating conditions to calculate its real-gas properties.")

    database = load_database()
    eos_names = ["van der Waals", "Redlich-Kwong", "Soave-Redlich-Kwong", "Peng-Robinson"]

    compound_names = list(database.keys())
    selected_name = st.selectbox("Compound", compound_names)
    properties = get_critical_properties(selected_name, database)

    eos_name = st.selectbox("Equation of State", eos_names, index=3)
    phase = st.selectbox("Phase", ["Vapour", "Liquid"])
    temperature = st.number_input("Temperature (K)", min_value=1.0, value=300.0, step=5.0)
    pressure_bar = st.number_input("Pressure (bar)", min_value=0.0001, value=10.0, step=1.0)

    # Pick a compound from the supplied table; its coefficients fill in automatically.
    cp_options = list(cp_database.keys())
    cp_name = st.selectbox("Heat-capacity data (Table C.1)", cp_options,
                           index=cp_options.index(selected_name) if selected_name in cp_options else 0)
    cp_A, cp_B, cp_C, cp_D = cp_database[cp_name]
    Tref = tempref
    Pref = pressref
    Href = 0.0
    Sref = 0.0

    if st.button("Calculate", use_container_width=True):
        try:
            pressure = pressure_bar * 1e5
            result = calculate_compressibility(pressure, temperature, properties, eos_name, phase)
            thermo = calculate_enthalpy_entropy(
                temperature, pressure, properties, eos_name, result["Z"],
                cp_A, cp_B, cp_C, cp_D, Tref, Pref, Href, Sref
            )

            st.subheader("Output")
            st.write("**Compressibility factor (Z):**", f'{result["Z"]:.6f}')
            st.write("**Molar volume (m³/mol):**", f'{result["V"]:.6e}')
            st.write("**Fugacity coefficient:**", f'{result["phi"]:.6f}')
            st.write("**Fugacity (bar):**", f'{result["fugacity"] / 1e5:.6f}')
            st.write("**Enthalpy (J/mol):**", f'{thermo["H"]:.6f}')
            st.write("**Entropy (J/mol·K):**", f'{thermo["S"]:.6f}')
        except Exception as error:
            st.error("The calculation did not finish: " + str(error))

    st.caption("Heat-capacity coefficients come from the supplied Table C.1. If a compound is missing there, choose another entry from the heat-capacity list.")


if __name__ == "__main__":
    main()

