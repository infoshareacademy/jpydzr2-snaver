## 1. Zainstaluj SQLAlchemy

pip install SQLAlchemy

## 2. Wyjaśnienia plików w katalogu database:

### mydatabase.py
plik database/mydatabase.py definiuje połączenie z bazą SQLite o nazwie foo.db - ale jeszcze nic z nią nie robi

### models.py
odpalenie pliku database/models.py tworzy nową bazę danych w katalogu /database o nazwie "foo.db" (jeśli wcześniej takiej nie było) ze schematem (tabelami) na podstawie klas zawartych w tym pliku

### populate.py
odpalenie pliku tworzy kilka instancji klasy User i wkleja je do bazy danych

### get.py
Przykładowe pozyskanie instancji klasy User z bazy danych

## 3. Uruchomienie i przetestowanie co i jak
Wystarczy odpalic pliki models, populate i get w tej kolejności