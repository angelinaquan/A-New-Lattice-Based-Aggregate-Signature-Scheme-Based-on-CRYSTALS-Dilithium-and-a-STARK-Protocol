"""Implementation of NTT for polynomials in Z_q[x]/(phi), such that q = 8380417 and phi = x ** n + 1, with n = 256
Functions are defined to perform polynomial operations with polynomials in NTT domain representation
"""

from supp_algs import split, merge

n = 256
q = 8380417
inv_2 = 4190209 #the inverse of 2 in q
sqr1 = 1479 #the square root of 1 mod q

#roots of 512-th unity
roots = [1663, 10626, 1777, 10512, 1426, 10863, 4654, 7635, 5291, 6998, 2704, 9585, 4938, 7351, 3636, 8653, 3915, 8374, 2166, 10123, 113, 12176, 4919, 7370, 3, 12286, 4437, 7852, 160, 12129, 3149, 9140, 4057, 8232, 3271, 9018, 1689, 10600, 3364, 8925, 4372, 7917, 2174, 10115, 4414, 7875, 2847, 9442, 2645, 9644, 4053, 8236, 2305, 9984, 5042, 7247, 5195, 7094, 2780, 9509, 1484, 10805, 4895, 7394, 3016, 9273, 243, 12046, 3000, 9289, 671, 11618, 3136, 9153, 5191, 7098, 2399, 9890, 3400, 8889, 2178, 10111, 1544, 10745, 420, 11869, 5559, 6730, 476, 11813, 3531, 8758, 3985, 8304, 4905, 7384, 5332, 6957, 3510, 8779, 2370, 9919, 2865, 9424, 2969, 9320, 3978, 8311, 2686, 9603, 3247, 9042, 4048, 8241, 2249, 10040, 1153, 11136, 2884, 9405, 5407, 6882, 3186, 9103, 1630, 10659, 2126, 10163, 2187, 10102, 2566, 9723, 2422, 9867, 6039, 6250, 2987, 9302, 6022, 6267, 2437, 9852, 3646, 8643, 875, 11414, 3780, 8509, 1607, 10682, 4976, 7313, 5011, 7278, 1002, 11287, 4284, 8005, 5088, 7201, 3248, 9041, 1207, 11082, 1168, 11121, 5277, 7012, 1065, 11224, 2143, 10146, 404, 11885, 4645, 7644, 1912, 10377, 1378, 10911, 435, 11854, 4337, 7952, 2381, 9908, 5444, 6845, 4096, 8193, 493, 11796, 545, 11744, 5019, 7270, 3704, 8585, 2678, 9611, 1537, 10752, 242, 12047, 4714, 7575, 4143, 8146, 27, 12262, 3066, 9223, 3763, 8526, 1440, 10849, 5084, 7205, 1632, 10657, 1017, 11272, 4885, 7404, 3778, 8511, 3833, 8456, 390, 11899, 773, 11516, 2401, 9888, 442, 11847, 5101, 7188, 1067, 11222, 2912, 9377, 5698, 6591, 354, 11935, 4861, 7428, 2859, 9430, 1045, 11244, 5012, 7277, 2481, 9808]

#list of inverses of each element in modulo q
inverses = []
for i in range(8380417):
    inverses.append(pow(i, -1, q))

def split_ntt(f_ntt):
    n = len(f_ntt)
    w = roots[n]
    f0_ntt = [0] * (n // 2)
    f1_ntt = [0] * (n // 2)
    for i in range(n // 2):
        f0_ntt[i] = (inv_2 * (f_ntt[2 * i] + f_ntt[2 * i + 1])) % q
        f1_ntt[i] = (inv_2 * (f_ntt[2 * i] - f_ntt[2 * i + 1]) * inverses[w[2 * i]]) % q
    return [f0_ntt, f1_ntt]


def merge_ntt(f_list_ntt):
    f0_ntt, f1_ntt = f_list_ntt
    n = 2 * len(f0_ntt)
    w = roots[n]
    f_ntt = [0] * n
    for i in range(n // 2):
        f_ntt[2 * i + 0] = (f0_ntt[i] + w[2 * i] * f1_ntt[i]) % q
        f_ntt[2 * i + 1] = (f0_ntt[i] - w[2 * i] * f1_ntt[i]) % q
    return f_ntt


def ntt(f):
    n = len(f)
    if (n > 2):
        f0, f1 = split(f)
        f0_ntt = ntt(f0)
        f1_ntt = ntt(f1)
        f_ntt = merge_ntt([f0_ntt, f1_ntt])
    elif (n == 2):
        f_ntt = [0] * n
        f_ntt[0] = (f[0] + sqr1 * f[1]) % q
        f_ntt[1] = (f[0] - sqr1 * f[1]) % q
    return f_ntt


def intt(f_ntt):
    n = len(f_ntt)
    if (n > 2):
        f0_ntt, f1_ntt = split_ntt(f_ntt)
        f0 = intt(f0_ntt)
        f1 = intt(f1_ntt)
        f = merge([f0, f1])
    elif (n == 2):
        f = [0] * n
        f[0] = (inv_2 * (f_ntt[0] + f_ntt[1])) % q
        f[1] = (inv_2 * inverses[1479] * (f_ntt[0] - f_ntt[1])) % q
    return f


def add_zq(f, g):
    assert len(f) == len(g)
    deg = len(f)
    return [(f[i] + g[i]) % q for i in range(deg)]


def neg_zq(f): #Negation of a polynomial
    deg = len(f)
    return [(- f[i]) % q for i in range(deg)]

def mul_zq(f, g): #Multiplication of two polynomials"""
    return intt(mul_ntt(ntt(f), ntt(g)))


def div_zq(f, g): #Division of two polynomials"""
    try:
        return intt(div_ntt(ntt(f), ntt(g)))
    except ZeroDivisionError:
        raise

def add_ntt(f_ntt, g_ntt): #Addition of two polynomials (NTT representation)."""
    return add_zq(f_ntt, g_ntt)

def mul_ntt(f_ntt, g_ntt): #Multiplication of two polynomials (coefficient representation)."""
    assert len(f_ntt) == len(g_ntt)
    deg = len(f_ntt)
    return [(f_ntt[i] * g_ntt[i]) % q for i in range(deg)]

def div_ntt(f_ntt, g_ntt): #Division of two polynomials (NTT representation)
    assert len(f_ntt) == len(g_ntt)
    deg = len(f_ntt)
    if any(elt == 0 for elt in g_ntt):
        raise ZeroDivisionError
    return [(f_ntt[i] * inverses[g_ntt[i]]) % q for i in range(deg)]

ntt_ratio = 1 #ratio between degree n ad the number of complex coefficients of the nTT