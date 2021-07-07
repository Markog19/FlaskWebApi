from datetime import datetime
from functools import wraps
from flask import request,jsonify
import models
import jwt
from init import db,app


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"Poruka":"Token ne postoji"}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],"HS256")
            trenutni_korisnik = models.Korisnik.query.filter_by(id=data['id']).first()
        except:
            return jsonify({"poruka":"Nepravilan token"}),401
        return f(trenutni_korisnik,*args,**kwargs)
    return decorated
def fillTable(route,id,f):
    novaAktivnost = models.Aktivnost(id_korisnika = id, vrijeme=datetime.now(),trajanje = f,ruta = route)
    db.session.add(novaAktivnost)
    db.session.commit()
    return jsonify({"Poruka":"Tablica ispunjena"})