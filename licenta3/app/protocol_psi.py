import time
from sqlalchemy import text
from app import db
from app.criptatre_date import decrypt_data, private_key, public_key
from app.models import Institutie

from app.psi.client import generate_random_numbers, mascare_date, intersection
from app.psi.server import bloom_filter, semneaza_datele


def see_intersection(cnp_encrypt, user_institution_id):
    start_time = time.time()  # start timing
    intersected_hospitals = []

    try:
        search_cnp = decrypt_data(private_key, cnp_encrypt)
        search_cnp_int = int(search_cnp)

        other_institutions = Institutie.query.filter(Institutie.id != user_institution_id).all()

        random_factors = generate_random_numbers(public_key)

        for institution in other_institutions:
            other_table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'
            query = text(f"SELECT cnp FROM {other_table_name}")
            results = db.session.execute(query).fetchall()

            bf = bloom_filter(private_key, [int(decrypt_data(private_key, result.cnp)) for result in results])

            A = mascare_date([search_cnp_int], random_factors, public_key.n)
            B = semneaza_datele(private_key, A)

            S = intersection(B, random_factors, public_key.n)

            for s in S:
                if s in bf:
                    intersected_hospitals.append(f"{institution.nume} - {institution.adresa}")
                    break

    except Exception as e:
        raise e

    end_time = time.time()  # end timing
    print(f"see_intersection execution time: {end_time - start_time} seconds")

    return intersected_hospitals
