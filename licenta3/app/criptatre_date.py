import base64
import os

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def generate_rsa_keys(private_key_path, public_key_path, n_bits=2048, exponent=65537):
    key = RSA.generate(n_bits, e=exponent)
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


def encrypt_data(public_key, data):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_b64


def decrypt_data(private_key, encrypted_data):
    try:
        encrypted_data = encrypted_data + '=' * (-len(encrypted_data) % 4)
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_bytes).decode('utf-8')
        return decrypted_data
    except Exception as e:
        raise e
