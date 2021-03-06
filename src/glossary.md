- **Budget**  - dla mnie budżet to kwota, którą mam do wykorzystania w danej kategorii, ale w naszych schematach funkcjonuje to inaczej, więc do ustalenia

- **to-be-budgeted** - miejsce, do którego trafiają dochody ze wszystkich kont Account. Kwota do rozdysponowania w ramach Category. Instancja klasy Category

- **Parent Category** - nadkategoria. W niej zawierają się Category. Nie są do niej przypisywane budżety ani wydatki. Wyświetlana kwota to suma kwot zawierających się w niej Category.

- **Category** - kategoria budżetowa, "koperta". Do Category przypisujemy kwoty z to-be-budgeted oraz wydatki.

- **Account** - konto bankowe, portfel z gotówką, pokazuje gdzie składowane są pieniądze, ale nie wpływa to na kwoty w Category.

- **Transaction** - przepływ "wirtualnej" kwoty, kwoty zabudżetowanej. Nie jest zależne od Account. Przepływ pomiędzy Category. 

- **Transfer** - przpływ monet, prawdziwego pieniądza. Dochód, wydatek .

- **Spending** - wydatki przypisane do Category. Pomniejszają budżet do wykorzystania w danej Category.

- **Income** - dochód. Każdy przypływ pieniądza. Przypisywany do Account - gotówka, konto w banku itd., od razu w instancji "To-be-budgeted".