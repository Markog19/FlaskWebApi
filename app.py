from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import time
import models 
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/testnabaza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)



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


@app.route('/register',methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['lozinka'],method='sha256')
    novi_korisnik = models.Korisnik(ime = data['ime'], prezime = data['prezime'], email = data['email'], korisnicko_ime = data['korisnicko_ime'], lozinka = hashed_password,status = True)
    db.session.add(novi_korisnik)
    db.session.commit()
    return jsonify({'poruka':'Korisnik uspjesno kreiran'})
@app.route('/user/activate',methods=['PUT'])
@token_required
def activate_user(trenutni_korisnik):
    start_time = time.time()
    if not trenutni_korisnik or trenutni_korisnik.status:
        end_time = time.time()
        fillTable("/user/activate",trenutni_korisnik.id,end_time-start_time)
        return jsonify({"Poruka":"Pogreska"})
    db.session.query(models.Korisnik).filter(
        models.Korisnik.korisnicko_ime == trenutni_korisnik.korisnicko_ime).update({
        models.Korisnik.status:True},synchronize_session=False)           
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
    

    db.session.query(models.Korisnik).filter(
        models.Korisnik.ime == trenutni_korisnik.ime).update(
        {models.Korisnik.status:False},synchronize_session=False)           
    db.session.commit()   
    end_time = time.time()
    fillTable("/user",trenutni_korisnik.id,end_time-start_time)     
    return jsonify({"Poruka":trenutni_korisnik.ime,"Time":str(end_time-start_time)})


@app.route('/login',methods=['GET'])
def login():
    start_time = time.time()
    auth = request.authorization
    
    korisnik = models.Korisnik.query.filter_by(korisnicko_ime = auth.username).first()
    if not korisnik.status:
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"poruka":"Status korisnika je 0, login nije moguc"})
    if not korisnik:
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"Poruka":"Pogreska"})
    if check_password_hash(korisnik.lozinka, auth.password):
        token = jwt.encode({
            'id': korisnik.id, 
            'exp':datetime.utcnow() + timedelta(hours=10)},
            app.config['SECRET_KEY'],algorithm="HS256"),
        end_time = time.time()
        fillTable("/login",korisnik.id,end_time - start_time)

        return jsonify({"token": token})
    

@app.route('/index',methods=['GET'])
def get_users():
    output = []
    uvjet = request.get_json()
    korisnici = None
    korisnik = None
    if uvjet==None:
        korisnici = models.Korisnik.query.all()
    elif uvjet['filter'] =="ime":
        korisnici = models.Korisnik.query.filter_by(ime = uvjet['search'])
    elif uvjet['filter'] == "prezime":
        korisnici = models.Korisnik.query.filter_by(prezime = uvjet['search'])

    elif uvjet['filter'] == "email":
        korisnici = models.Korisnik.query.filter_by(email = uvjet['search'])
   
    elif uvjet['filter'] == "korisnicko_ime":
        korisnici = models.Korisnik.query.filter_by(korisnicko_ime = uvjet['search'])
    elif uvjet['filter'] == "status":
        korisnici = models.Korisnik.query.filter_by(status = uvjet['search'])
    
    for korisnik in korisnici:
        data = {
            "ime":korisnik.ime,
            "prezime":korisnik.prezime,
            "email":korisnik.email,
            "korisnicko_ime":korisnik.korisnicko_ime,
            "lozinka":korisnik.lozinka,
            "status":korisnik.status
                }
       
        output.append(data)
   
    return jsonify({'users' : output})



@app.route('/user',methods=['POST'])



@app.route('/user',methods=['PUT'])
def update_user():
    start_time = time.time()

    data = request.get_json()
    trenutniKorisnik = models.Korisnik.query.filter_by(ime = data['ime']).first()
    if not trenutniKorisnik:
        return jsonify({"Poruka":"Korisnik ne postoji"})
    if(check_password_hash(trenutniKorisnik.lozinka,data['stara_lozinka'])):
        if(data['nova_lozinka'] == data['potvrdi_novu']):
            db.session.query(models.Korisnik).filter(models.Korisnik.ime == data['ime']).update({models.Korisnik.lozinka:generate_password_hash(data['nova_lozinka'])},synchronize_session=False)           
        else:
            fillTable("/user")
            return jsonify({"Poruka":"Lozinke nisu iste"})
    else:
        end_time = time.time()

        fillTable("/user",trenutniKorisnik.id,end_time-start_time)
        return jsonify({"Poruka":"Pogresna Lozinka"})
    
    db.session.commit()   
    end_time = time.time()
     
    fillTable("/user",trenutniKorisnik.id,end_time-start_time)
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
    obj = {
        'start' : start,
        'limit' : limit,
        'count' : count,
    }
  
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
    aktivnosti = models.Aktivnost.query.filter_by(id_korisnika = podatci['id'])
    korisnici = models.Korisnik.query.filter_by(id = podatci['id'])
    for korisnik in korisnici:
        for aktivnost in aktivnosti:
            output.append({
                'ime': korisnik.ime,
                'id_korisnika' : aktivnost.id_korisnika,
                'vrijeme' : aktivnost.vrijeme,
                'trajanje' : aktivnost.trajanje,
                'ruta' : aktivnost.ruta,
                })
        if(start>len(output)):
            return jsonify({"Poruka":"Ne postoji vise unosa"})
    return jsonify({"Output":get_paginated_list(output,"/activites",start,limit,per_page=5)})

@app.route('/home')
def homepage():
    return jsonify({"data":"data"})
if __name__ =="__main__":
    app.run(debug = True,host='localhost',threaded=True)