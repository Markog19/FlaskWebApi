from flask import Flask,Request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from app import Korisnik,Aktivnost,app,db

@app.route('/register',methods=['POST'])
def create_user():
    data = Request.get_json()
    hashed_password = generate_password_hash(data['lozinka'],method='sha256')
    novi_korisnik = Korisnik(ime = data['ime'], prezime = data['prezime'], email = data['email'], korisnicko_ime = data['korisnicko_ime'], lozinka = hashed_password,status = False)
    db.session.add(novi_korisnik)
    db.session.commit()
    return jsonify({'poruka':'Korisnik uspjesno kreiran'})


@app.route('/user/activate ',methods=['PUT'])
def activate_user():
    return ''



@app.route('/user',methods=['DELETE'])
def delete_user():
    return



@app.route('/login',methods=['GET'])
def login():
    return



@app.route('/index',methods=['GET'])
def get_users():
    return



@app.route('/user',methods=['POST'])



@app.route('/user',methods=['PUT'])
def update_user():
    return


@app.route('/activites',methods=['GET'])
def get_activities():
    return




