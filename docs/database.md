## 1. Wymagania

`pip install SQLAlchemy`

ewentualnie:

`pip install -r src/requirements.txt`

## 2. Wyjaśnienie plików związanych z bazą danych

#### database.py, session.py w katalogu głównym
pliki definiujące bazę danych i ustanawiające sesję

#### models/models.py
Modele klas

#### create-tables.py w katalogu głównym
odpalenie pliku tabele na podstawie zaimportowanych modeli

#### populate.py
Plik (docelowo) wypełniający bazę danych testowymi rekordami

#### test-queries.py
Plik, w którym możemy testować zapytania do bazy

## 3. Materiały

* [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)