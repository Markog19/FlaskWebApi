# FlaskWebApi

1.    /registration POST (ime, prezime, email, korisnicko ime i  lozinka) - gotovo samo jos mail

        Kreira se novi korisnik u bazi sa statusom 0

        Poslati korisniku na mail aktivacijski link. Link se sastoji od id korisnika i JWT tokena

        Lozinku spremiti u hash formatu

2.  /user/activate PUT (id_korisnika, jwt_token) - gotovo

        Logika servisa provjerava je li token validan, ako je token validan potrebno je korisniku promijeniti status na 1, što znači da je on od tog trenutka aktivan. Ako token nije validan onda servis vraća odgovarajuću poruku.

3.  /user DELETE (id_korisnika) - gotovo

        Provjera JWT tokena

        Mjenja status korisnika na 0

4.   /login GET - (username,password) - gotovo

        Provjera korisničkog imena i lozinke

        Provjera aktivnosti korisnika (ne može se logirati ako je deaktiviran)

        Na ovom servisu se izdaje JWT token

        Spremi zapis u tablicu aktivnosti

5.    /index GET (search) - gotovo

        Javna ruta dostupna svima

        Vraća sve korisnike unutar sustava

        Omogućuje pretraživanje po svim poljima osim passwordu

6.    /user POST (ime, prezime, email,korisnicko ime i lozinka) - nisam siguran koja je razlika u funkciji ove i registration

        Provjera JWT tokena

        Provjera jedinstvenosti email-a i username

        Kreira se korisnik sa statusom 0 (Neaktivan)

        Poslati na mail aktivacijski link 

7.   /user PUT (Ime, prezime, stara_lozinka, nova_lozinka, potvrdi_novu) - gotovo

8.    /activites Može GET ili POST (id_korisnika, search,date_from, date_to, start, page_size) - gotovo

        Vratiti sve aktivnosti za korisnika sortitane po datumu kreiranja

        Pomoću start i page_size parametara napraviti paginaciju

        Voditi računa da se u responsu prikaže i ime korisnika, a ne samo id korisnika
