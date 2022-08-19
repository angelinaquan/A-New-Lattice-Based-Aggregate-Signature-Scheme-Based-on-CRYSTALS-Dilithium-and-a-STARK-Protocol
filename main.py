'''This file sets parameters of our LAS scheme and define necessary classes'''

import numpy as np
from numpy import set_printoptions
from supp_algs import HighestBit
import hashlib
from ntt import mul_ntt,add_ntt

hashfunc = hashlib.shake_256()
import sys
if sys.version_info >= (3, 4):
    from importlib import reload

set_printoptions(linewidth=200, precision=5, suppress=True)
n = 256
q = 8380417

class UniformDilithiumParameterSet(object):
    def __init__(self, n, k, l, gamma1, gamma2, tau, q, eta, beta, beta1, omega, lambd, n_sig, pkdrop=0):
        self.n = n
        self.k = k
        self.l = l
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.q = q
        self.eta = eta
        self.zeta = max(gamma1, 2*gamma2 + 1 + 2**(pkdrop-1)*tau)
        self.zeta_prime = max(2*gamma1, 4*gamma2 + 1)
        self.pkdrop = pkdrop
        self.beta = beta
        self.beta1 = beta1
        self.omega = omega
        self.lambd = lambd
        self.n_sig = n_sig

class PublicKey:
    def __init__(self, sk):
        self.n = sk.n
        self.h = sk.h
        self.A = np.random.random((5, 4))
        self.t_1 = HighestBit(add_ntt(mul_ntt(self.A,sk.s_1) + sk.s_2))
        self.hash_to_point = sk.hash_to_point
        self.signature_bound = sk.signature_bound

    def __repr__(self):
        rep = "Public for n = {n}:\n\n".format(n=self.n)
        rep += "h = {h}\n".format(h=self.h)
        return rep


class SecretKey:
    def __init__(self, s_1, s_2, polys=None):
        """Initialize a secret key."""
        self.n = n
        self.sigma = Params[n]["sigma"]
        self.sigmin = Params[n]["sigmin"]
        self.signature_bound = Params[n]["sig_bound"]
        self.sig_bytelen = Params[n]["sig_bytelen"]
        self.s_1 = s_1
        self.s_2 = s_2

    def __repr__(self, verbose=False):
        rep = "Private key for n = {n}:\n\n".format(n=self.n)
        rep += "s_1 = {s_1}\n".format(s_1=self.s_1)
        rep += "s_2 = {s_2}\n".format(s_2=self.s_2)
        return rep

    def hash_to_point(self, message,salt):
        k = (1 << 16) // q
        shake = hashlib.shake_256()
        shake.update(salt)
        shake.update(message)
        hash = [0 for i in range(n)]
        i = 0
        j = 0
        while i < n:
            twoB = shake.digest_size(2)
            elt = (twoB[0] << 8) + twoB[1]
            if elt < k * q:
                hash[i] = elt % q
                i += 1
            j += 1
        return hash