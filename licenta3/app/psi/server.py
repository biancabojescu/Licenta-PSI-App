import time

from app.psi.functii_utile import BloomFilter


def decrypt(key, element):
    d, n = key.d, key.n
    return pow(element, d, n)


def bloom_filter(pv_key, X, size=1000, hash_count=10):
    start_time = time.time()
    bf = BloomFilter(size, hash_count)

    for x in X:
        decrypted_element = str(decrypt(pv_key, x))
        bf.add(decrypted_element)

    end_time = time.time()
    print(f"bloom_filter execution time: {end_time - start_time} seconds")
    return bf


def semneaza_datele(pv_key, A):
    start_time = time.time()  # start timing
    B = []
    for a in A:
        B.append(decrypt(pv_key, a))

    end_time = time.time()  # end timing
    print(f"semneaza_datele execution time: {end_time - start_time} seconds")
    return B


def update_bf(bf, pv_key, P, X):
    start_time = time.time()  # start timing
    for i in P:
        decrypted_element = str(decrypt(pv_key, X[i]))
        bf.add(decrypted_element)

    end_time = time.time()  # end timing
    print(f"update_bf execution time: {end_time - start_time} seconds")


def insert_elements_bf(bf, pv_key, U):
    start_time = time.time()  # start timing
    for u in U:
        decrypted_element = str(decrypt(pv_key, u))
        bf.add(decrypted_element)

    end_time = time.time()  # end timing
    print(f"insert_elements_bf execution time: {end_time - start_time} seconds")
