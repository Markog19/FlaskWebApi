from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
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

@app.route('/')
def homepage():
    return 'hello world'
if __name__ =="__main__":
    app.run(debug = True,host='localhost',threaded=True)