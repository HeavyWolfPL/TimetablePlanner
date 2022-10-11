# TimetablePlanner
---
### Proces generowania planu
1. Iteracja po wszystkich klasach
2. Iteracja po każdej godzinie lekcyjnej
3. Dobór przedmiotu i nauczyciela
4. Sprawdzenie czy przydzielony nauczyciel jest wolny
5. Wpisanie przedmiotu do planu
6. Powrót do punktu 2

![Schemat generowania planu lekcji](docs/Diagram.png)

---

### Wymagania
- Python 3.10+

<details>
<summary>Pakiety</summary>

```yml
Placeholder
Placeholder
```

</details>

---

### To-Do

<details>
<summary>Wersja 1.0</summary>

#### 1. Baza danych
> - [ ] Tabele:
>   - [x] Nauczyciele
>   - [x] Przedmioty
>   - [x] Klasy
>   - [x] Sale
>   - [ ] Plan lekcji
> - [ ] Wprowadzenie zabezpieczeń przed idiotyczną zmianą danych
> - [ ] MS Access -> SQL -> phpMyAdmin
> - [ ] Dostęp z serwera
> - [ ] Wprowadzenie samych danych

#### 2. Generator
> - [ ] Generowanie planu na gotowych danych
> - [ ] Przydzielanie sali do klasy na bazie wolnych sal i liczby osób
> - [ ] Przydzielenie nauczyciela do klasy na bazie etatu
> - [ ] Połączenie z bazą danych
> - [ ] Zapis danych tymczasowo jako XML/JSON
> - [ ] Komunikacja przez PyScript

#### 3. Strona
> - [ ] Prototyp wyglądu strony na bazie placeholderowych tabelek
> - [ ] Panel wprowadzania danych do bazy (?)
> - [ ] Umożliwienie przeglądu danych z bazy
> - [ ] Połączenie z bazą danych
> - [ ] Wyświetlenie danych na czysto lub odczytanie z XML/JSON (?)
> - [ ] Wyświetlenie danych w tabeli
> - [ ] Panel wyboru
>   - [ ] Klasy
>   - [ ] Nauczyciela
>   - [ ] Sali

</details>

<details>
<summary>Wersja 2.0</summary>

> - [ ] Wsparcie roczników IV - VIII
> - [ ] Wsparcie klas ukierunkowanych

</details>