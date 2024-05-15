from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Institutie(db.Model):
    __tablename__ = 'institutii'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    adresa = Column(String(255))
    users = relationship("User", back_populates="institutie")
    pacienti = relationship("Pacienti", back_populates="institutie")

    def __repr__(self):
        return f'<Institutie {self.nume}>'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    prenume = Column(String(255))
    email = Column(String(255), unique=True)
    profesie = Column(String(255))
    parola = Column(String(255))
    is_auth = Column(Boolean, default=False)
    role = Column(String(50), default='user')
    id_institutie = Column(Integer, ForeignKey('institutii.id'))
    institutie = relationship("Institutie", back_populates="users")

    def __repr__(self):
        return f'<User {self.nume} {self.prenume}>'

class Pacienti(db.Model):
    __tablename__ = 'pacienti'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    prenume = Column(String(255))
    data_nastere = Column(String(255))
    varsta = Column(Integer)
    cnp = Column(String(255), unique=True)
    sex = Column(String(255))
    fisa_medicala = Column(String(255))
    nr_telefon = Column(String(255))
    email = Column(String(255), unique=True)
    adresa = Column(String(255))
    id_institutie = Column(Integer, ForeignKey('institutii.id'))
    institutie = relationship("Institutie", back_populates="pacienti")

    def __repr__(self):
        return f'<Pacient {self.nume} {self.prenume}>'
