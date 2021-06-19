# FlaskWebApi

1. /registration POST (ime, prezime, email, korisnicko ime i  lozinka)
    - potrebno riješiti slanje mail-a

2. /user/activate PUT (id_korisnika, jwt_token) 


3. /user DELETE (id_korisnika)


4. /login GET - (username,password)


5. /index GET (search) 
    - napravljen osnovni search, potrebno dodat filter

6. /user PUT (Ime, prezime, stara_lozinka, nova_lozinka, potvrdi_novu) - zavrseno

7. /activites Može GET ili POST (id_korisnika, search,date_from, date_to, start, page_size) 
