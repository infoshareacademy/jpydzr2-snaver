## 1. Zainstaluj SQLAlchemy

`pip install SQLAlchemy`

ewentualnie:

`pip install -r src/requirements.txt`

## 2. Wyjaśnienie plików w katalogu database:

#### mydatabase.py
plik mydatabase.py definiuje połączenie z bazą SQLite o nazwie foo.db - ale jeszcze nic z nią nie robi

#### models.py
odpalenie pliku models.py tworzy nową bazę danych w katalogu database (jeśli wcześniej takiej nie było) ze schematem (tabelami) na podstawie klas zawartych w tym pliku

#### populate.py
odpalenie pliku tworzy kilka przykładowych instancji klasy User i wkleja je do bazy danych

#### get.py
Przykładowe pozyskanie instancji klasy User z bazy danych

## 3. Uruchomienie i przetestowanie co i jak
Wystarczy odpalic pliki models, populate i get w tej kolejności

## 4. Materiały

* [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)