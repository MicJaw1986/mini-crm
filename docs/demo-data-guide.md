# 📊 Przewodnik po danych demonstracyjnych

## 🎯 Czym są dane demonstracyjne?

**Dane demonstracyjne** to przykładowe rekordy w bazie danych, które pozwalają:
- Przetestować aplikację bez ręcznego wprowadzania danych
- Zaprezentować funkcjonalność systemu klientom/managerom
- Zrozumieć jak dane wyglądają w prawdziwym użyciu
- Nauczyć się obsługi systemu na realnych przykładach

## 🚀 Jak wygenerować dane?

### Komenda podstawowa
```bash
python manage.py generate_demo_data
```

### Komenda z czyszczeniem starych danych
```bash
python manage.py generate_demo_data --clear
```

### Wybór liczby użytkowników
```bash
python manage.py generate_demo_data --users 5
```

### Pomoc
```bash
python manage.py generate_demo_data --help
```

## 📋 Co zostaje wygenerowane?

### 1. **Użytkownicy (3 domyślnie)**
- **Login**: `demo1`, `demo2`, `demo3`
- **Hasło**: `demo123` (dla wszystkich)
- **Email**: `demo1@minicrm.pl`, etc.
- **Imiona i nazwiska**: Losowe polskie imiona

**UWAGA**: W produkcji NIGDY nie używaj prostych haseł jak `demo123`!

### 2. **Firmy (12)**
Przykładowe firmy IT/biznesowe:
- Tech Solutions Sp. z o.o.
- Digital Marketing Pro
- Innowacyjne Systemy IT
- Consulting Partners
- E-Commerce Masters
- ...i więcej

**Dla każdej firmy**:
- NIP (losowy 10-cyfrowy)
- Branża (IT, Marketing, Consulting, E-commerce, Finance, Healthcare, Education)
- Adres (ulica, kod pocztowy, miasto)
- Strona WWW
- Właściciel (losowo przypisany użytkownik demo)

### 3. **Kontakty (45)**
Polskie imiona i nazwiska:
- Jan Kowalski, Anna Nowak, Piotr Wiśniewski, etc.

**Dla każdego kontaktu**:
- Imię i nazwisko
- Email (unikalny)
- Telefon i komórka (polskie numery)
- Firma (80% ma przypisaną firmę)
- Stanowisko (CEO, CTO, Marketing Manager, etc.)
- Status:
  - **40%** - customer (klient)
  - **30%** - lead (potencjalny klient)
  - **25%** - prospect (zainteresowany)
  - **5%** - churned (utracony)
- Tagi: vip, partner, nowy klient, etc.
- Notatki

### 4. **Interakcje (80)**
Historia kontaktów z klientami:

**Typy interakcji**:
- Email (np. "Oferta handlowa", "Pytanie o produkt")
- Telefon (np. "Konsultacja techniczna", "Follow-up")
- Spotkanie (np. "Prezentacja produktu", "Demo systemu")
- Notatka (np. "Ważna informacja wewnętrzna")

**Szczegóły**:
- Data: Losowa w ciągu ostatnich 90 dni
- Opis: Realistyczny opis działania
- Ważność: 15% oznaczonych jako ważne
- Przypisanie: Do kontaktu LUB firmy

### 5. **Zadania (35)**
Do zrobienia dla zespołu:

**Przykładowe zadania**:
- Przygotuj ofertę handlową
- Zadzwoń do klienta - follow-up
- Przygotuj prezentację produktu
- Umówić spotkanie demo
- Wysłać newsletter
- Zorganizować webinar

**Status zadań**:
- **40%** - todo (do zrobienia)
- **30%** - in_progress (w trakcie)
- **25%** - done (wykonane)
- **5%** - cancelled (anulowane)

**Priorytety**:
- **50%** - medium (średni)
- **25%** - high (wysoki)
- **20%** - low (niski)
- **5%** - urgent (pilny)

**Terminy**:
- Zadania wykonane: termin w przeszłości
- Zadania aktywne: 30% przeterminowane, 70% w przyszłości (1-60 dni)

## 🔐 Logowanie do systemu

Po wygenerowaniu danych możesz zalogować się jako:

| Login  | Hasło    | Email            |
|--------|----------|------------------|
| demo1  | demo123  | demo1@minicrm.pl |
| demo2  | demo123  | demo2@minicrm.pl |
| demo3  | demo123  | demo3@minicrm.pl |

## 📊 Statystyki wygenerowanych danych

| Typ danych    | Liczba | Opis                                    |
|---------------|--------|-----------------------------------------|
| Użytkownicy   | 3      | Użytkownicy testowi z hasłem demo123   |
| Firmy         | 12     | Polskie firmy IT/biznesowe             |
| Kontakty      | 45     | Osoby z polskimi imionami              |
| Interakcje    | 80     | Historia kontaktów (90 dni wstecz)     |
| Zadania       | 35     | Zadania w różnych statusach            |

## 🧪 Użycie w testach

### Scenariusz 1: Prezentacja dla klienta
1. Wygeneruj dane: `python manage.py generate_demo_data --clear`
2. Zaloguj się jako `demo1` / `demo123`
3. Pokaż dashboard ze statystykami
4. Przejdź do listy kontaktów - 45 przykładowych rekordów
5. Otwórz szczegóły kontaktu - zobacz interakcje i zadania

### Scenariusz 2: Testowanie funkcjonalności
1. Zaloguj się jako różni użytkownicy (demo1, demo2, demo3)
2. Sprawdź izolację danych - każdy widzi tylko swoje kontakty
3. Przetestuj wyszukiwanie - jest dużo rekordów do przeszukania
4. Przetestuj filtrowanie po statusie, firmie
5. Sprawdź przeterminowane zadania na dashboardzie

### Scenariusz 3: Szkolenie użytkowników
1. Każdy uczestnik dostaje login (demo1, demo2, demo3)
2. Może pracować na gotowych danych
3. Może dodawać własne kontakty i zadania
4. Po szkoleniu: `--clear` i generuj od nowa

## ⚠️ Ważne uwagi

### Czyszczenie danych
Opcja `--clear` usuwa **TYLKO** użytkowników zaczynających się od "demo":
- ✅ Usuwa: demo1, demo2, demo3
- ❌ NIE usuwa: admin, superuser, prawdziwych użytkowników

### Kaskadowe usuwanie
Gdy usuwasz użytkownika demo, Django automatycznie usuwa:
- Jego kontakty (przez `owner` ForeignKey)
- Jego firmy
- Jego zadania
- Jego interakcje

Dzieje się to dzięki `on_delete=models.CASCADE` w modelach.

### Bezpieczeństwo
- W produkcji NIE używaj prostego hasła `demo123`
- Dane demo nie zawierają wrażliwych informacji
- Wszystkie dane są losowe i fikcyjne

## 🛠️ Jak działa komenda?

### Management Command
Komenda to plik Python w folderze `management/commands/`:
```
contacts/
└── management/
    └── commands/
        └── generate_demo_data.py
```

### Główne funkcje:
1. `create_users()` - tworzy użytkowników testowych
2. `create_companies()` - generuje firmy
3. `create_contacts()` - tworzy kontakty
4. `create_interactions()` - dodaje historię interakcji
5. `create_tasks()` - generuje zadania

### Wykorzystane techniki:
- `random.choice()` - losowy wybór z listy
- `random.randint()` - losowa liczba
- `random.random()` - losowy float 0-1
- `random.choices(weights=...)` - wybór z wagami
- `timezone.now()` - aktualna data z timezone
- `timedelta()` - operacje na datach

## 📚 Następne kroki

Po wygenerowaniu danych możesz:
1. ✅ Zalogować się i eksplorować aplikację
2. ✅ Przetestować wszystkie funkcje CRUD
3. ✅ Sprawdzić dashboard i statystyki
4. ✅ Wypróbować wyszukiwanie i filtrowanie
5. ✅ Dodać własne dane do istniejących
6. ✅ Przećwiczyć tworzenie raportów

## 🎓 Co się nauczyłeś?

- Czym są Management Commands w Django
- Jak generować realistyczne dane testowe
- Jak używać modułu `random` do losowania
- Jak pracować z datami (`timezone`, `timedelta`)
- Jak tworzyć relacje między obiektami
- Jak używać ForeignKey w praktyce
- Jak działają operacje kaskadowe w bazie danych

---

**Pro tip**: Regularnie regeneruj dane demo przed prezentacjami, żeby mieć czyste, spójne dane!
