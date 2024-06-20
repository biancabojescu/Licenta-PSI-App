import secrets
import time

from app.psi.functii_utile import extended_gcd, mod_inverse


def generate_random_elements(NC):
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

    end_time = time.time()
    print(f"generate_random_numbers execution time: {end_time - start_time} seconds")
    return rand_nums


def mascare_date(Y, rand_nums, n):
    start_time = time.time()

    A = [(rf[1] * y) % n for y, rf in zip(Y, rand_nums)]

    end_time = time.time()
    print(f"mascare_date execution time: {end_time - start_time} seconds")
    return A


def intersection(B, rand_nums, n):
    start_time = time.time()

    S = [(b * rf[0]) % n for b, rf in zip(B, rand_nums)]

    end_time = time.time()
    print(f"intersection execution time: {end_time - start_time} seconds")
    return S
