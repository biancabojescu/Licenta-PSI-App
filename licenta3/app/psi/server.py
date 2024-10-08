import time
from concurrent.futures.thread import ThreadPoolExecutor

from app.psi.functii_utile import BloomFilter

'''
def decrypt(key, element):
    d, n = key.d, key.n
    return pow(element, d, n)
'''


def decrypt(key, element):
    d, n = key.d, key.n
    p, q = key.p, key.q
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = pow(q, -1, p)

    m1 = pow(element, dp, p)
    m2 = pow(element, dq, q)

    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q

    return m


def bloom_filter(pv_key, X, size=10000, hash_count=10):
    start_time = time.time()
    bf = BloomFilter(size, hash_count)

    with ThreadPoolExecutor() as executor:
        decrypted_elements = list(executor.map(lambda x: str(decrypt(pv_key, x)), X))

    for x in decrypted_elements:
        bf.add(x)

    end_time = time.time()
    print(f"bloom_filter execution time: {end_time - start_time} seconds")
    return bf


def semneaza_datele(pv_key, A):
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        B = list(executor.map(lambda a: decrypt(pv_key, a), A))

    end_time = time.time()  # end timing
    print(f"semneaza_datele execution time: {end_time - start_time} seconds")
    return B
