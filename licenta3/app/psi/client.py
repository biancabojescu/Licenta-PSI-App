import secrets
import time

from app.psi.functii_utile import extended_gcd, mod_inverse
from app.psi.server import decrypt


def generate_random_elements(NC):
    while True:
        r = secrets.randbelow(NC)
        gcd, _, _ = extended_gcd(r, NC)
        if gcd == 1:
            return r


def encrypt(key, element):
    e, n = key.e, key.n
    return pow(element, e, n)


def generate_random_numbers(pb_key, NC_max=1024):
    start_time = time.time()
    rand_nums = []

    for _ in range(NC_max):
        r = generate_random_elements(pb_key.n)
        r_inv = mod_inverse(r, pb_key.n)
        r_encrypt = encrypt(pb_key, r)
        rand_nums.append((r_inv, r_encrypt))

    end_time = time.time()  # end timing
    print(f"generate_random_numbers execution time: {end_time - start_time} seconds")
    return rand_nums


def mascare_date(Y, rand_nums, n):
    start_time = time.time()  # start timing
    A = []
    for y, rf in zip(Y, rand_nums):
        r_encrypt = rf[1]
        A.append((r_encrypt * y) % n)

    end_time = time.time()  # end timing
    print(f"mascare_date execution time: {end_time - start_time} seconds")
    return A


def intersection(B, rand_nums, n):
    start_time = time.time()  # start timing
    S = []
    for b, rf in zip(B, rand_nums):
        r_inv = rf[0]
        S.append((b * r_inv) % n)

    end_time = time.time()  # end timing
    print(f"intersection execution time: {end_time - start_time} seconds")
    return S


def generate_update_positions(n, NU_max=100):
    update_positions = []
    for _ in range(NU_max):
        update_positions.append(secrets.randbelow(n))
    return update_positions


def modify_bloom_filter(bf, P, pv_key, U):
    start_time = time.time()  # start timing
    for i in P:
        bf.add(decrypt(pv_key, U[i]))

    end_time = time.time()  # end timing
    print(f"modify_bloom_filter execution time: {end_time - start_time} seconds")
