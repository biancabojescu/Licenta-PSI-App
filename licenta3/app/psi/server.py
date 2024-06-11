from app.psi.functii_utile import BloomFilter


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
