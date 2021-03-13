## 1. Wymagania

`pip install SQLAlchemy`

ewentualnie:

`pip install -r src/requirements.txt`

## 2. Wyjaśnienie plików związanych z bazą danych

#### database.py, session.py
pliki definiujące bazę danych i ustanawiające sesję - można o nich na razie zapomnieć

#### models/models.py
Modele klas

#### db-create-tables.py
odpalenie pliku tworzy tabele na podstawie zaimportowanych modeli

#### db-populate.py
Plik wypełniający bazę danych testowymi rekordami

#### db-test-queries.py
Plik, w którym możemy testować zapytania do bazy

## 3. Postawienie bazy
Odpalenie db-create-tables, potem db-populate (jeśli chcemy mieć testowe dane)
Ew. później db-test-queries do debugowania

Baza teraz ma rozszerzenie .sqlite - działa o wiele lepiej niż wcześniej, gdy miała rozszerzenie .db

## 4. Materiały

* [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)