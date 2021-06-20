from flask import Flask
from flask.json import dump
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql.selectable import TableClause
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import date, datetime, timedelta
from functools import wraps
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/testnabaza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
class Korisnik(db.Model):
    id = Column(Integer,primary_key=True)
    ime = Column(String(50))
    prezime = Column(String(50))
    email = Column(String(50))
    korisnicko_ime = Column(String(50))
    lozinka = Column(String(200))
    status = Column(Boolean)




class Aktivnost(db.Model):
    id = Column(Integer,primary_key=True)
    id_korisnika = Column(Integer)
    vrijeme = Column(DateTime)
    trajanje = Column(Float)
    ruta = Column(String(50))

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"Poruka":"Token ne postoji"}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            trenutni_korisnik = Korisnik.query.filter_by(id=data['id']).first()
        except:
            return jsonify({"poruka":"Nepravilan token"}),401
        return f(trenutni_korisnik,*args,**kwargs)
    return decorated
def fillTable(route,id,f):
    novaAktivnost = Aktivnost(id_korisnika = id, vrijeme=datetime.now(),trajanje = f,ruta = route)
    db.session.add(novaAktivnost)
    db.session.commit()
    return jsonify({"Poruka":"Tablica ispunjena"})




@app.route('/register',methods=['POST'])
def create_user():
    start_time = datetime.now()
    data = request.get_json()
    hashed_password = generate_password_hash(data['lozinka'],method='sha256')
    novi_korisnik = Korisnik(ime = data['ime'], prezime = data['prezime'], email = data['email'], korisnicko_ime = data['korisnicko_ime'], lozinka = hashed_password,status = False)
    db.session.add(novi_korisnik)
    db.session.commit()
    end_time = datetime.now()
    fillTable("/register",novi_korisnik.id,end_time-start_time)
    return jsonify({'poruka':'Korisnik uspjesno kreiran'})
@app.route('/user/activate',methods=['PUT'])
@token_required
def activate_user(trenutni_korisnik):
    start_time = time.time()
    if not trenutni_korisnik or trenutni_korisnik.status:
        end_time = time.time()
        fillTable("/user/activate",trenutni_korisnik.id,end_time-start_time)
        return jsonify({"Poruka":"Pogreska"})
    db.session.query(Korisnik).filter(Korisnik.ime == trenutni_korisnik.ime).update({Korisnik.status:True},synchronize_session=False)           
    db.session.commit()
    end_time = time.time()   
    fillTable("/user/activate",trenutni_korisnik.id,end_time-start_time)
     
    return jsonify({"Poruka":trenutni_korisnik.ime})


@app.route('/user',methods=['DELETE'])
@token_required
def delete_user(trenutni_korisnik):
    start_time = time.time()

    if not trenutni_korisnik or not trenutni_korisnik.status:
        end_time = time.time()
        fillTable("/user",trenutni_korisnik.id,end_time-start_time)     
        return jsonify({"Poruka":"Pogreska","trajanje":end_time-start_time})
    

    db.session.query(Korisnik).filter(Korisnik.ime == trenutni_korisnik.ime).update({Korisnik.status:False},synchronize_session=False)           
    db.session.commit()   
    end_time = time.time()
    fillTable("/user",trenutni_korisnik.id,end_time-start_time)     
    return jsonify({"Poruka":trenutni_korisnik.ime,"Time":str(end_time-start_time)})




@app.route('/login',methods=['GET'])
def login():
    start_time = time.time()
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"Poruka":"Pogreska"})
    korisnik = Korisnik.query.filter_by(ime = auth.username).first()
    if not korisnik.status:
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"poruka":"Status korisnika je 0, login nije moguc"})
    if not korisnik:
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"Poruka":"Pogreska"})
    if check_password_hash(korisnik.lozinka, auth.password):
        token = jwt.encode({'id': korisnik.id, 'exp':datetime.utcnow() + timedelta(hours=10)},app.config['SECRET_KEY'],algorithm="HS256")
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"token": token})
    


@app.route('/index/',methods=['GET'])
def get_users():
    output = []
    uvjet = request.get_json()
    korisnici = None
    korisnik = None
    if uvjet['filter'] =="ime":
        korisnici = Korisnik.query.filter_by(ime = uvjet['search'])
    elif uvjet['filter'] == "prezime":
        korisnici = Korisnik.query.filter_by(prezime = uvjet['search'])

    elif uvjet['filter'] == "email":
        korisnici = Korisnik.query.filter_by(email = uvjet['search'])
   
    elif uvjet['filter'] == "korisnicko_ime":
        korisnici = Korisnik.query.filter_by(korisnicko_ime = uvjet['search'])
    elif uvjet['filter'] == "status":
        korisnici = Korisnik.query.filter_by(status = uvjet['search'])

    for korisnik in korisnici:
        data = {}
        data['ime'] = korisnik.ime
        data['prezime'] = korisnik.prezime
        data['email'] = korisnik.email
        data['korisnicko_ime'] = korisnik.korisnicko_ime
        data['lozinka'] = korisnik.lozinka
        data['status'] = korisnik.status
        output.append(data)
   
    return jsonify({'users' : output})



@app.route('/user',methods=['POST'])



@app.route('/user',methods=['PUT'])
def update_user():
    data = request.get_json()
    trenutniKorisnik = Korisnik.query.filter_by(ime = data['ime']).first()
    if not trenutniKorisnik:
        return jsonify({"Poruka":"Korisnik ne postoji"})
    if(check_password_hash(trenutniKorisnik.lozinka,data['stara_lozinka'])):
        if(data['nova_lozinka'] == data['potvrdi_novu']):
            db.session.query(Korisnik).filter(Korisnik.ime == data['ime']).update({Korisnik.lozinka:generate_password_hash(data['nova_lozinka'])},synchronize_session=False)           
        else:
            fillTable("/user")
            return jsonify({"Poruka":"Lozinke nisu iste"})
    else:
        fillTable("/user",trenutniKorisnik.id)
        return jsonify({"Poruka":"Pogresna Lozinka"})
    
    db.session.commit()        
    fillTable("/user")
    return jsonify({
        "poruka":"Uspjesno"
    })

def get_paginated_list(results, url, start, limit,per_page):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if  limit < 0:
        return jsonify({"Poruka":"Ne postoji vise unosa"})
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '/%d/%d' % (start_copy, limit_copy)
    # make next url
    if start  > count:
        obj['next'] = ''
    else:
        start_copy = start + per_page
        obj['next'] = url + '/%d/%d' % (start_copy, limit+per_page)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

@app.route('/activites/<int:start>/<int:limit>',methods=['GET'])
def get_activities(start,limit):
    podatci = request.get_json()
    output = []
    aktivnosti = Aktivnost.query.filter_by(id_korisnika = podatci['id'])
    korisnici = Korisnik.query.filter_by(id = podatci['id'])
    for korisnik in korisnici:
        
        for aktivnost in aktivnosti:
            data = {}
            data['ime'] = korisnik.ime
            
            data['id_korisnika'] = aktivnost.id_korisnika
            data['vrijeme'] = aktivnost.vrijeme
            data['trajanje'] = aktivnost.trajanje
            data['ruta'] = aktivnost.ruta
            output.append(data)
        if(start>len(output)):
            return jsonify({"Poruka":"Ne postoji vise unosa"})


    return jsonify({"Output":get_paginated_list(output,"/activites",start,limit,per_page=5)})

@app.route('/home')
def homepage():
    return jsonify({"data":"data"})
if __name__ =="__main__":
    app.run(debug = True,host='localhost',threaded=True)