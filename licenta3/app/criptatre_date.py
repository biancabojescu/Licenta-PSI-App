import base64
import os
from Crypto.Util.number import getPrime, inverse, long_to_bytes, long_to_bytes
from Crypto.PublicKey import RSA


def generate_rsa_keys(private_key_path, public_key_path, n_bits=2048, exponent=65537):
    # Generăm două prime mari p și q
    p = getPrime(n_bits // 2)
    q = getPrime(n_bits // 2)

    # Calculăm n și phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Calculăm cheia publică e și cheia privată d
    e = exponent
    d = inverse(e, phi)

    # Calculăm CRT params
    dP = d % (p - 1)
    dQ = d % (q - 1)
    qInv = inverse(q, p)

    # Exportăm cheile
    key = RSA.construct((n, e, d, p, q, dP, dQ, qInv))
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_key_path, "wb") as priv_file:
        priv_file.write(private_key)

    with open(public_key_path, "wb") as pub_file:
        pub_file.write(public_key)


private_key_path = ("C:/Users/bianc/OneDrive/Desktop/Facultate/Anul3/Licenta/Licenta-PSI-App/licenta3/app"
                    "/chei_criptare/private.pem")
public_key_path = ("C:/Users/bianc/OneDrive/Desktop/Facultate/Anul3/Licenta/Licenta-PSI-App/licenta3/app/chei_criptare"
                   "/public.pem")

if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
    generate_rsa_keys(private_key_path, public_key_path)

with open(private_key_path, "rb") as priv_file:
    private_key = RSA.import_key(priv_file.read())

with open(public_key_path, "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())


def crt_decrypt(private_key, encrypted_data):
    n = private_key.n
    p = private_key.p
    q = private_key.q
    dP = private_key.d % (p - 1)
    dQ = private_key.d % (q - 1)
    qInv = private_key.u

    m1 = pow(encrypted_data, dP, p)
    m2 = pow(encrypted_data, dQ, q)
    h = (qInv * (m1 - m2)) % p
    m = m2 + h * q
    return m


def decrypt_data(private_key, encrypted_data):
    try:
        encrypted_data = encrypted_data + '=' * (-len(encrypted_data) % 4)
        encrypted_bytes = base64.b64decode(encrypted_data)
        encrypted_int = int.from_bytes(encrypted_bytes, byteorder='big')
        decrypted_int = crt_decrypt(private_key, encrypted_int)
        decrypted_data = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')
        try:
            decrypted_text = decrypted_data.decode('utf-8')
            return decrypted_text
        except UnicodeDecodeError as e:
            raise ValueError("Decrypted data is not valid UTF-8")
    except Exception as e:
        raise e


def encrypt_data(public_key, data):
    data_bytes = data.encode('utf-8')
    data_int = int.from_bytes(data_bytes, byteorder='big')
    encrypted_int = pow(data_int, public_key.e, public_key.n)
    encrypted_bytes = encrypted_int.to_bytes((public_key.n.bit_length() + 7) // 8, byteorder='big')
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_b64

