# Nazewnictwo

- **Budget** - Całe konto gdzie są wszystkie kategorie, wydatki etc.

- **ParentCategory** - nadkategoria. W niej zawierają się Category. Nie są do niej przypisywane budżety ani wydatki. Wyświetlana kwota to suma kwot zawierających się w niej Category.

- **Category** - kategoria budżetowa, "koperta". Do Category przypisujemy kwoty z to-be-budgeted oraz wydatki.

    - **available_amount** - Kwota jaka została w kategorii
      
    - **budgeted_amount** - Kwota jaką maksymalnie chcemy wydać w tej kategorii
    
- **Transaction** - przpływ monet, prawdziwego pieniądza. Transakcja może być wpływem (np wypłata) lub wydatkiem (opłata rachunku)
    
    - **inflow** - Ile pieniędzy wpłynęło na konto
      
    - **outflow** - Ile wydaliśmy z konta