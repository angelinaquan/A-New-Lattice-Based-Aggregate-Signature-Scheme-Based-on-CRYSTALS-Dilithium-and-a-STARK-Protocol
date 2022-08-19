'''This files includes the five main algorithms of our proposed lAS scheme:
KeyGen, Sign, Verify, AggSig, and AggSigVerify'''

import hashlib
hashfunc = hashlib.shake_256()
import numpy as np
from Crypto.Hash import SHAKE256
from ntt import mul_ntt, add_ntt
from supp_algs import perpendicular, HighestBit, LowestBit #Define these functions
shake = SHAKE256.new()

from main import UniformDilithiumParameterSet, PublicKey, SecretKey
UniformDilithium = UniformDilithiumParameterSet(n, 4, 4, 5*2**17, (q-1)/32, 39, q, 2, 175, 250, 120, 235, 2759, pkdrop=13)

def KeyGen():
    s_1 = np.random.random_integers(0,UniformDilithium.eta,6)
    s_2 = np.random.random_integers(0,UniformDilithium.eta,5)
    sk = SecretKey(s_1,s_2)
    pk = PublicKey(sk)
    return pk, sk

def Sign(sk, M):
    A = np.random.random((5, 4))
    shake.update(M)
    mu = shake.read(384)
    z = None
    h = None
    c = None
    while perpendicular(z,h):
        y = np.random.random_integers(0,UniformDilithium.gamma1 - 1,6)
        w = mul_ntt(A,y)
        w_1 = HighestBit(w,2*UniformDilithium.gamma2)
        shake2 = SHAKE256.new()
        shake2.update(w_1)
        shake2.update(mu)
        c = SHAKE256.read(60)
        z = y + c * sk.s_1
        if z.bit_length() < UniformDilithium.gamma1 - UniformDilithium.beta:
            t_0 = LowestBit(add_ntt(mul_ntt(A,sk.s_1) + sk.s_2))
            h= Make(-c*t_0,w-c*sk.s_2+c*t_0,2*UniformDilithium.gamma2)
    sigma = (z,h,c)
    return (sigma)

def Verify(pk, M, sig):
    A = pk.A
    shake.update(M)
    shake2 = SHAKE256.new()
    shake2.update(pk.t_1)
    shake.update(shake2.read())
    mu = shake.read(384)

    y = np.random.random_integers(0, UniformDilithium.gamma1 - 1, 6)
    w = mul_ntt(A, y)
    w_1 = HighestBit(w, 2 * UniformDilithium.gamma2)

    z_val = sig[0].bit_length() < UniformDilithium.gamma1 - UniformDilithium.beta
    h_val = sig[1].bit_length() <= UniformDilithium.omega
    if hashfunc(w_1,mu) == sig[2]:
        c_val = True
    else:
        c_val = False

    sigma_val = z_val and h_val and c_val
    return sigma_val

def AggSig(PK,M,sig_set):
    z_agg = None
    c_agg = None
    h_agg = None
    for i in range(UniformDilithium.n_sig):
        shake.update(PK[i])
        shake.update(M[i])
        v = shake.read()
        z_agg += Sign(PK[i],M[i])[0] * v
        h_agg += Sign(PK[i], M[i])[1]
        c_agg += Sign(PK[i], M[i])[2] * v

    agg_sig = (z_agg, h_agg, c_agg)
    return agg_sig

def AggSigVerify(PK,M,AggSig):

    v_sum = None

    for i in range(UniformDilithium.n_sig):
        shake.update(PK[i])
        shake.update(M[i])
        v = shake.read()
        v_sum += v

    z_agg_val = AggSig[0] <= (UniformDilithium.lambd - UniformDilithium.beta) * v_sum
    c_agg_val = AggSig[2] == v_sum * hashfunc(w_i, mu_i)
    h_agg_val = AggSig[1] <= UniformDilithium.n_sig * UniformDilithium.omega^{1/2}

    agg_sig_val = z_agg_val and h_agg_val and c_agg_val
    return agg_sig_val