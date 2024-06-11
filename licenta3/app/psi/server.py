class BitArray:
    def __init__(self, size):
        self.size = size
        self.array = [0] * size

    def set(self, index):
        if 0 <= index < self.size:
            self.array[index] = 1
        else:
            raise IndexError("Index out of range")

    def clear(self, index):
        if 0 <= index < self.size:
            self.array[index] = 0
        else:
            raise IndexError("Index out of range")

    def get(self, index):
        if 0 <= index < self.size:
            return self.array[index]
        else:
            raise IndexError("Index out of range")

    def setall(self, value):
        if value not in [0, 1]:
            raise ValueError("Value must be 0 or 1")
        self.array = [value] * self.size

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        if value not in [0, 1]:
            raise ValueError("Value must be 0 or 1")
        if 0 <= index < self.size:
            self.array[index] = value
        else:
            raise IndexError("Index out of range")

    def __repr__(self):
        return ''.join(map(str, self.array))


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = BitArray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        item_str = str(item)
        hash_values = []
        for i in range(self.hash_count):
            # Hash simplu: suma și multiplicarea caracterelor cu un offset
            hash_value = 0
            for char in item_str:
                hash_value = (hash_value * 31 + ord(char) + i) % self.size
            hash_values.append(hash_value)
        return hash_values

    def add(self, item):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

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
