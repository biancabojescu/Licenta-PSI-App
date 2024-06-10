import hashlib
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        item_str = str(item)
        return [int(hashlib.md5((item_str + str(i)).encode('utf-8')).hexdigest(), 16) % self.size for i in
                range(self.hash_count)]

    def add(self, item):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = True

    def __contains__(self, item):
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))


def decrypt(key, element):
    d, n = key.d, key.n
    return pow(element, d, n)


def bloom_filter(pv_key, X, size=1000, hash_count=10):
    bf = BloomFilter(size, hash_count)

    for x in X:
        decrypted_element = str(decrypt(pv_key, x))
        bf.add(decrypted_element)

    return bf


def semneaza_datele(pv_key, A):
    B = []
    for a in A:
        B.append(decrypt(pv_key, a))
    return B


def update_bf(bf, pv_key, P, X):
    for i in P:
        decrypted_element = str(decrypt(pv_key, X[i]))
        bf.add(decrypted_element)


def insert_elements_bf(bf, pv_key, U):
    for u in U:
        decrypted_element = str(decrypt(pv_key, u))
        bf.add(decrypted_element)
