'''This file defines some supplemental/support algorithms that are used as parts of other algorithms'''

import numpy as np

def split(f):
    n = len(f)
    f0 = [f[2 * i + 0] for i in range(n // 2)]
    f1 = [f[2 * i + 1] for i in range(n // 2)]
    return [f0, f1]


def merge(f_list):
    f0, f1 = f_list
    n = 2 * len(f0)
    f = [0] * n
    for i in range(n // 2):
        f[2 * i + 0] = f0[i]
        f[2 * i + 1] = f1[i]
    return f


def HighestBit(*n):
    if (n == 0):
        return 0
    msb = 0
    n = n / 2

    while (n != 0):
        n = n / 2
        msb += 1
    return (1 << msb)


def LowestBit(*n):
        return (n & -n).bit_length() - 1


def perpendicular(x,y) :
    z = np.empty_like(x)
    z[0] = -x[1]
    z[1] = x[0]
    if (y == z):
        return True
    else:
        return False
