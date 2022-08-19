'''This files tests whether everything is implemented correctly
The final results (signature size and public key size) is also generated after this file runs properly
'''

from winterfell import prover, verifier
from main_algs import KeyGen, Sign, Verify, AggSig, AggSigVerify
from sys import getsizeof
from main import UniformDilithiumParameterSet

UniformDilithium = UniformDilithiumParameterSet(n, 4, 4, 5*2**17, (q-1)/32, 39, q, 2, 175, 250, 120, 235, 2759, pkdrop=13)
PK = []
SK = []

for i in range(UniformDilithium.n_sig):
    pk, sk = KeyGen()
    PK.append(pk)
    SK.append(sk)

M = [] #set of messages/transactions vary for different situations

sig_set = []

for i in range(UniformDilithium.n_sig):
    sig_set.append(Sign(SK[i]),M[i])

agg_sig = AggSig(PK,M,sig_set)

if AggSigVerify(PK,M,agg_sig) != True
    print("Something went wrong. ")

for i in range(UniformDilithium.n_sig):
    check = Verify(PK[i],M[i],Sign(SK[i],M[i]))
    if check != True
        print("Something went wrong. ")

proof = prover(UniformDilithium,(256,M,PK),sig_set)
valid = verifier(UniformDilithium,(256,M,PK),agg_sig)

if valid != True
    print("Something went wrong. ")

print("The size of the public key is ", getsizeof(PK))
print("The signature size is ", getsizeof(AggSig))