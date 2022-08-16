# A New Lattice-Based Aggregate Signature Scheme Based on CRYSTALS-Dilithium and a STARK Protocol
Implementation Code for the Research Project "Improving Bitcoin's Post-Quantum Transaction Efficiency with Novel Lattice-Based Aggregate Signature Scheme Based on CRYSTALS-Dilithium and a STARK Protocol" by Yunjia Quan

**WARNING**: Note that this is a research project. It has not been audited and may contain bugs or flaws. This implementation is NOT ready for production use.

## Content
This repository contains the following files: 
- [main.py](main.py) sets parameters and define necessary classes
- [main_algs.py](main_algs.py) contains the five-tuple of the main algorithms which makes up our proposed LAS scheme
- [ntt.py](ntt.py) implements NTT domain representation for all polynomials in modulo q
- [test.py](test.py) ensures that everything is implemented properly
- [supp_algs.py](supp_algs.py) includes supplemental/support algorithms that we use for other functions

## References
[1] Ducas, L., Kiltz, E., Lepoint, T., Lyubashevsky, V., Schwabe, P., Seiler, G., & Stehlé, D. (2018). Crystals-dilithium: A lattice-based digital signature scheme. IACR Transactions on Cryptographic Hardware and Embedded Systems, 238-268. https://eprint.iacr.org/2017/633.pdf. 

[2] Khaburzaniya, I., Chalkias, K., Lewi, K., & Malvai, H. (2022, May). Aggregating and thresholdizing hash-based signatures using STARKs. In Proceedings of the 2022 ACM on Asia Conference on Computer and Communications Security (pp. 393-407). https://eprint.iacr.org/2021/1048.pdf.

[3] Boneh, D., & Kim, S. (2020). One-Time and Interactive Aggregate Signatures from Lattices. https://crypto.stanford.edu/~skim13/agg_ots.pdf.

#### Repository References
[4] https://github.com/pq-crystals/dilithium

[5] https://github.com/pq-crystals/security-estimates

[6] https://github.com/tprest/falcon.py
