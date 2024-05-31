import pybloom_live
from Crypto.PublicKey import RSA


def decrypt(key, element):
    d, n = key.d, key.n
    return pow(element, d, n)


def bloom_filter(pv_key, X):
    mode = pybloom_live.ScalableBloomFilter.SMALL_SET_GROWTH
    bf = pybloom_live.ScalableBloomFilter(mode=mode)

    for x in X:
        bf.add(decrypt(pv_key, x))

    return bf


def sign_batch(pv_key, A):
    B = []
    for a in A:
        B.append(decrypt(pv_key, a))
    return B


def update_bloom_filter(bf, pv_key, P, X):
    for i in P:
        bf.add(decrypt(pv_key, X[i]))


def insert_new_elements(bf, pv_key, U):
    for u in U:
        bf.add(decrypt(pv_key, u))
