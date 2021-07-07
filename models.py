
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from sqlalchemy import Column, Integer, String
from init import db
class Korisnik(db.Model):
    id = Column(Integer,primary_key=True)
    ime = Column(String(50))
    prezime = Column(String(50))
    email = Column(String(50))
    korisnicko_ime = Column(String(50),unique=True)
    lozinka = Column(String(200))
    status = Column(Boolean)

    def __init__(self,ime,prezime,email,korisnicko_ime,lozinka,status):
        self.ime = ime
        self.prezime = prezime
        self.email = email
        self.korisnicko_ime = korisnicko_ime
        self.lozinka = lozinka
        self.status = status

class Aktivnost(db.Model):
    id = Column(Integer,primary_key=True)
    id_korisnika = Column(Integer)
    vrijeme = Column(DateTime)
    trajanje = Column(Float)
    ruta = Column(String(50))

    def __init__(self,id_korisnika,vrijeme,trajanje,ruta):
        self.id_korisnika = id_korisnika
        self.vrijeme = vrijeme
        self.trajanje = trajanje
        self.ruta = ruta
