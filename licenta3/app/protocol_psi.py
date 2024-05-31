import logging
from sqlalchemy import text
from app import db
from app.criptatre_date import decrypt_data, private_key, public_key
from app.models import Institutie

from app.psi.client import generate_random_numbers, blind_batch, verify_batch
from app.psi.server import bloom_filter, sign_batch


def see_intersection(cnp_encrypt, user_institution_id):
    intersected_hospitals = []

    try:
        # Decrypt the search CNP
        search_cnp = decrypt_data(private_key, cnp_encrypt)
        search_cnp_int = int(search_cnp)

        # Get all institutions except the current user's institution
        other_institutions = Institutie.query.filter(Institutie.id != user_institution_id).all()

        # Step 1: Generate random numbers
        random_factors = generate_random_numbers(public_key)

        for institution in other_institutions:
            other_table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'
            query = text(f"SELECT cnp FROM {other_table_name}")
            results = db.session.execute(query).fetchall()

            # Step 2: Initialize bf
            bf = bloom_filter(private_key, [int(decrypt_data(private_key, result.cnp)) for result in results])

            # Step 3: Client blinding, Server signing
            A = blind_batch([search_cnp_int], random_factors, public_key.n)
            B = sign_batch(private_key, A)

            # Step 4: Client verification
            S = verify_batch(B, random_factors, public_key.n)

            # Check if the CNP is in the Bloom filter
            for s in S:
                if s in bf:
                    intersected_hospitals.append(institution.nume)
                    break

    except Exception as e:
        logging.error(f"Error in see_intersection: {e}")

    return intersected_hospitals
