from flask import Flask
from flask.json import dump
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import update


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/testnabaza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    vrijeme = Column(DateTime)
    trajanje = Column(Integer)
    ruta = Column(String(50))

@app.route('/register',methods=['POST'])
def create_user():
    data = request.get_json()
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



@app.route('/index/',methods=['GET'])
def get_users():
    output = []
    uvjet = request.get_json()
    korisnici = Korisnik.query.all()
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
            return jsonify({"Poruka":"Lozinke nisu iste"})
    else:
        return jsonify({"Poruka":"Pogresna Lozinka"})
    
    db.session.commit()        


   

    return jsonify({
        "poruka":"Uspjesno"
    })


@app.route('/activites',methods=['GET'])
def get_activities():
    return

@app.route('/home')
def homepage():
    return jsonify({"data":"data"})
if __name__ =="__main__":
    app.run(debug = True,host='localhost',threaded=True)