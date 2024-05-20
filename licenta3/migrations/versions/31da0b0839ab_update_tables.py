"""Update tables

Revision ID: 31da0b0839ab
Revises: d0567c11245b
Create Date: 2024-05-20 18:07:52.697535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31da0b0839ab'
down_revision = 'd0567c11245b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pacienti_parhon')
    op.drop_table('pacienti_providența')
    op.drop_table('pacienti_spitalul_de_copii_sf_maria')
    op.drop_table('pacienti_spitalul_clinic_județean_de_urgențe_sf_spiridon_')
    op.drop_table('pacienti_spitalul_clinic_cfr')
    op.drop_table('pacienti_arcadia')
    with op.batch_alter_table('pacienti', schema=None) as batch_op:
        batch_op.drop_constraint('pacienti_cnp_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pacienti', schema=None) as batch_op:
        batch_op.create_unique_constraint('pacienti_cnp_key', ['cnp'])

    op.create_table('pacienti_arcadia',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_arcadia_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_arcadia_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_arcadia_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_arcadia_email_key')
    )
    op.create_table('pacienti_spitalul_clinic_cfr',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_spitalul_clinic_cfr_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_spitalul_clinic_cfr_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_spitalul_clinic_cfr_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_spitalul_clinic_cfr_email_key')
    )
    op.create_table('pacienti_spitalul_clinic_județean_de_urgențe_sf_spiridon_',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"pacienti_spitalul_clinic_județean_de_urgențe_sf_spirid_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_spitalul_clinic_județean_de_urgențe_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_spitalul_clinic_județean_de_urgențe_sf_spiridon_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_spitalul_clinic_județean_de_urgențe_sf_spiri_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_spitalul_clinic_județean_de_urgențe_sf_spi_email_key')
    )
    op.create_table('pacienti_spitalul_de_copii_sf_maria',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_spitalul_de_copii_sf_maria_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_spitalul_de_copii_sf_maria_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_spitalul_de_copii_sf_maria_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_spitalul_de_copii_sf_maria_email_key')
    )
    op.create_table('pacienti_providența',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"pacienti_providența_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_providența_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_providența_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_providența_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_providența_email_key')
    )
    op.create_table('pacienti_parhon',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('prenume', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data_nastere', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('varsta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cnp', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fisa_medicala', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nr_telefon', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('adresa', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_pacienti', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_pacienti'], ['pacienti.id'], name='pacienti_parhon_id_pacienti_fkey'),
    sa.PrimaryKeyConstraint('id', name='pacienti_parhon_pkey'),
    sa.UniqueConstraint('cnp', name='pacienti_parhon_cnp_key'),
    sa.UniqueConstraint('email', name='pacienti_parhon_email_key')
    )
    # ### end Alembic commands ###
