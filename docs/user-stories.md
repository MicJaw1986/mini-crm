# User Stories
## Mini CRM - System Zarządzania Relacjami z Klientami

**Wersja:** 1.0.0
**Data:** 2026-01-17

---

## Epic 1: Zarządzanie Kontem Użytkownika

### US-001: Rejestracja Użytkownika
**Jako** nowy użytkownik
**Chcę** zarejestrować się w systemie
**Aby** móc korzystać z funkcji CRM

**Kryteria Akceptacji:**
- [ ] Formularz rejestracji zawiera pola: username, email, password, password confirmation
- [ ] System waliduje unikalność username i email
- [ ] Hasło musi mieć minimum 8 znaków
- [ ] Po udanej rejestracji użytkownik jest automatycznie zalogowany
- [ ] Po rejestracji następuje przekierowanie na dashboard
- [ ] W przypadku błędów walidacji wyświetlane są komunikaty

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-002: Logowanie Użytkownika
**Jako** zarejestrowany użytkownik
**Chcę** się zalogować do systemu
**Aby** uzyskać dostęp do moich danych

**Kryteria Akceptacji:**
- [ ] Formularz logowania zawiera pola: username/email i password
- [ ] System weryfikuje poprawność danych logowania
- [ ] Po udanym logowaniu następuje przekierowanie na dashboard
- [ ] W przypadku błędnych danych wyświetlany jest komunikat błędu
- [ ] Link "Nie masz konta? Zarejestruj się" prowadzi do formularza rejestracji

**Priorytet:** MUST HAVE
**Punkty:** 2
**Status:** To Do

---

### US-003: Wylogowanie Użytkownika
**Jako** zalogowany użytkownik
**Chcę** się wylogować z systemu
**Aby** zabezpieczyć swoje konto

**Kryteria Akceptacji:**
- [ ] Przycisk "Wyloguj" dostępny w nawigacji
- [ ] Po kliknięciu użytkownik jest wylogowywany
- [ ] Następuje przekierowanie na stronę logowania
- [ ] Sesja użytkownika jest czyszczona
- [ ] Próba dostępu do chronionych stron przekierowuje na login

**Priorytet:** MUST HAVE
**Punkty:** 1
**Status:** To Do

---

### US-004: Profil Użytkownika
**Jako** zalogowany użytkownik
**Chcę** zobaczyć i edytować swój profil
**Aby** zarządzać moimi danymi osobowymi

**Kryteria Akceptacji:**
- [ ] Strona profilu wyświetla: username, email, datę rejestracji
- [ ] Użytkownik może zmienić email (z walidacją)
- [ ] Użytkownik może zmienić hasło (z potwierdzeniem)
- [ ] Zmiany są zapisywane po kliknięciu "Zapisz"
- [ ] Wyświetlane są komunikaty o sukcesie/błędzie

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

## Epic 2: Zarządzanie Kontaktami

### US-005: Lista Kontaktów
**Jako** użytkownik
**Chcę** zobaczyć listę wszystkich moich kontaktów
**Aby** mieć przegląd mojej bazy klientów

**Kryteria Akceptacji:**
- [ ] Lista wyświetla: imię, nazwisko, email, telefon, firmę, status
- [ ] Kontakty są sortowane po dacie ostatniej aktualizacji (najnowsze pierwsze)
- [ ] Paginacja po 20 kontaktów na stronę
- [ ] Każdy wiersz ma przyciski: Szczegóły, Edytuj, Usuń
- [ ] Widoczny przycisk "Dodaj nowy kontakt"
- [ ] Użytkownik widzi TYLKO swoje kontakty

**Priorytet:** MUST HAVE
**Punkty:** 5
**Status:** To Do

---

### US-006: Dodawanie Kontaktu
**Jako** użytkownik
**Chcę** dodać nowy kontakt
**Aby** przechowywać informacje o kliencie

**Kryteria Akceptacji:**
- [ ] Formularz zawiera pola: imię*, nazwisko*, email, telefon, pozycja, firma (dropdown), status, notatki
- [ ] Pola oznaczone * są wymagane
- [ ] Email jest walidowany jako poprawny adres
- [ ] Status domyślnie ustawiony na "Lead"
- [ ] Po zapisaniu następuje przekierowanie na szczegóły kontaktu
- [ ] Wyświetlany jest komunikat sukcesu

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-007: Edycja Kontaktu
**Jako** użytkownik
**Chcę** edytować istniejący kontakt
**Aby** zaktualizować jego dane

**Kryteria Akceptacji:**
- [ ] Formularz edycji jest wypełniony aktualnymi danymi
- [ ] Wszystkie pola są edytowalne
- [ ] Walidacja jak przy dodawaniu
- [ ] Po zapisaniu aktualizuje się `updated_at`
- [ ] Następuje przekierowanie na szczegóły kontaktu
- [ ] Wyświetlany jest komunikat sukcesu

**Priorytet:** MUST HAVE
**Punkty:** 2
**Status:** To Do

---

### US-008: Usuwanie Kontaktu
**Jako** użytkownik
**Chcę** usunąć kontakt
**Aby** pozbyć się nieaktualnych danych

**Kryteria Akceptacji:**
- [ ] Przed usunięciem wyświetlany jest modal potwierdzenia
- [ ] Po potwierdzeniu kontakt jest usuwany
- [ ] Wraz z kontaktem usuwane są jego interakcje i zadania
- [ ] Następuje przekierowanie na listę kontaktów
- [ ] Wyświetlany jest komunikat "Kontakt usunięty"

**Priorytet:** MUST HAVE
**Punkty:** 2
**Status:** To Do

---

### US-009: Wyszukiwanie Kontaktów
**Jako** użytkownik
**Chcę** wyszukać kontakt po imieniu lub nazwisku
**Aby** szybko znaleźć konkretną osobę

**Kryteria Akceptacji:**
- [ ] Pole wyszukiwania nad listą kontaktów
- [ ] Wyszukiwanie działa po: imieniu, nazwisku, emailu
- [ ] Wyniki są filtrowane w czasie rzeczywistym (lub po kliknięciu "Szukaj")
- [ ] Wyszukiwanie jest case-insensitive
- [ ] Jeśli brak wyników, wyświetlany jest komunikat "Nie znaleziono kontaktów"

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-010: Filtrowanie Kontaktów po Statusie
**Jako** użytkownik
**Chcę** filtrować kontakty według statusu
**Aby** zobaczyć np. tylko aktywnych klientów

**Kryteria Akceptacji:**
- [ ] Dropdown ze statusami: Wszystkie, Lead, Prospect, Customer, Churned
- [ ] Po wybraniu statusu lista jest filtrowana
- [ ] Liczba wyników jest widoczna (np. "Znaleziono: 15 kontaktów")
- [ ] Filtr można połączyć z wyszukiwaniem
- [ ] Można zresetować filtry (przycisk "Wyczyść")

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

### US-011: Szczegóły Kontaktu
**Jako** użytkownik
**Chcę** zobaczyć szczegóły kontaktu
**Aby** poznać pełną historię interakcji

**Kryteria Akceptacji:**
- [ ] Strona wyświetla wszystkie dane kontaktu
- [ ] Widoczna firma (jeśli przypisana) z linkiem
- [ ] Timeline interakcji w porządku chronologicznym (od najnowszych)
- [ ] Lista zadań przypisanych do kontaktu
- [ ] Przyciski: Edytuj, Usuń, Dodaj notatkę, Dodaj zadanie
- [ ] Przycisk "Generuj podsumowanie AI" (jeśli AI aktywne)

**Priorytet:** MUST HAVE
**Punkty:** 5
**Status:** To Do

---

## Epic 3: Zarządzanie Firmami

### US-012: Lista Firm
**Jako** użytkownik
**Chcę** zobaczyć listę firm
**Aby** zarządzać organizacjami

**Kryteria Akceptacji:**
- [ ] Lista wyświetla: nazwę, branżę, liczbę kontaktów
- [ ] Sortowanie alfabetyczne po nazwie
- [ ] Linki do szczegółów firmy
- [ ] Przycisk "Dodaj nową firmę"
- [ ] Użytkownik widzi tylko swoje firmy

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

### US-013: Dodawanie Firmy
**Jako** użytkownik
**Chcę** dodać nową firmę
**Aby** grupować kontakty według organizacji

**Kryteria Akceptacji:**
- [ ] Formularz zawiera: nazwę*, stronę www, branżę, adres
- [ ] Nazwa jest wymagana
- [ ] Strona www jest walidowana jako URL (jeśli podana)
- [ ] Po zapisaniu przekierowanie na szczegóły firmy

**Priorytet:** SHOULD HAVE
**Punkty:** 2
**Status:** To Do

---

### US-014: Edycja i Usuwanie Firmy
**Jako** użytkownik
**Chcę** edytować lub usunąć firmę
**Aby** zarządzać danymi organizacji

**Kryteria Akceptacji:**
- [ ] Edycja działa analogicznie do kontaktów
- [ ] Usunięcie firmy NIE usuwa przypisanych kontaktów (ustawia company=NULL)
- [ ] Modal potwierdzenia przed usunięciem

**Priorytet:** SHOULD HAVE
**Punkty:** 2
**Status:** To Do

---

### US-015: Szczegóły Firmy
**Jako** użytkownik
**Chcę** zobaczyć szczegóły firmy
**Aby** poznać przypisane kontakty

**Kryteria Akceptacji:**
- [ ] Wyświetlane są wszystkie dane firmy
- [ ] Lista kontaktów pracujących w tej firmie
- [ ] Linki do szczegółów kontaktów
- [ ] Liczba kontaktów w firmie
- [ ] Przyciski: Edytuj, Usuń

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

## Epic 4: Interakcje i Historia

### US-016: Dodawanie Interakcji do Kontaktu
**Jako** użytkownik
**Chcę** dodać notatkę/interakcję do kontaktu
**Aby** zapamiętać szczegóły rozmowy

**Kryteria Akceptacji:**
- [ ] Formularz dostępny na stronie szczegółów kontaktu
- [ ] Pola: typ interakcji (dropdown: Note, Call, Email, Meeting), treść*
- [ ] Treść jest wymagana (minimum 10 znaków)
- [ ] Po zapisaniu interakcja pojawia się w timeline
- [ ] Automatycznie ustawiany `created_at` (timestamp)
- [ ] Komunikat sukcesu

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-017: Timeline Interakcji
**Jako** użytkownik
**Chcę** zobaczyć chronologiczną historię interakcji
**Aby** śledzić komunikację z klientem

**Kryteria Akceptacji:**
- [ ] Interakcje wyświetlane od najnowszej do najstarszej
- [ ] Każda interakcja pokazuje: typ, datę, treść
- [ ] Ikona odpowiadająca typowi (telefon, email, spotkanie, notatka)
- [ ] Przycisk "Usuń" przy każdej interakcji
- [ ] Jeśli brak interakcji: "Brak historii. Dodaj pierwszą notatkę."

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-018: Usuwanie Interakcji
**Jako** użytkownik
**Chcę** usunąć interakcję
**Aby** pozbyć się błędnych wpisów

**Kryteria Akceptacji:**
- [ ] Przycisk "Usuń" przy każdej interakcji
- [ ] Modal potwierdzenia
- [ ] Po usunięciu znika z timeline
- [ ] Komunikat "Interakcja usunięta"

**Priorytet:** SHOULD HAVE
**Punkty:** 1
**Status:** To Do

---

## Epic 5: Zarządzanie Zadaniami

### US-019: Dodawanie Zadania
**Jako** użytkownik
**Chcę** utworzyć zadanie powiązane z kontaktem
**Aby** nie zapomnieć o follow-upie

**Kryteria Akceptacji:**
- [ ] Formularz zawiera: tytuł*, opis, kontakt (dropdown), termin, status
- [ ] Tytuł jest wymagany
- [ ] Status domyślnie "To Do"
- [ ] Termin może być pusty lub w przyszłości
- [ ] Po zapisaniu przekierowanie na listę zadań
- [ ] Komunikat sukcesu

**Priorytet:** MUST HAVE
**Punkty:** 3
**Status:** To Do

---

### US-020: Lista Wszystkich Zadań
**Jako** użytkownik
**Chcę** zobaczyć listę wszystkich moich zadań
**Aby** planować pracę

**Kryteria Akceptacji:**
- [ ] Lista wyświetla: tytuł, kontakt, termin, status
- [ ] Sortowanie: po terminie (najbliższe pierwsze)
- [ ] Filtrowanie po statusie (Todo, In Progress, Done)
- [ ] Zadania przeterminowane oznaczone kolorem czerwonym
- [ ] Linki do kontaktów
- [ ] Przycisk "Dodaj zadanie"

**Priorytet:** MUST HAVE
**Punkty:** 5
**Status:** To Do

---

### US-021: Zadania na Dziś (Dashboard)
**Jako** użytkownik
**Chcę** zobaczyć zadania zaplanowane na dzisiaj
**Aby** wiedzieć co mam do zrobienia

**Kryteria Akceptacji:**
- [ ] Widget na dashboardzie pokazuje zadania z `due_date = today`
- [ ] Wyświetlane są zadania w statusie "To Do" i "In Progress"
- [ ] Liczba zadań jest widoczna (np. "3 zadania na dziś")
- [ ] Checkbox do szybkiej zmiany statusu na "Done"
- [ ] Link "Zobacz wszystkie zadania"

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

### US-022: Zmiana Statusu Zadania
**Jako** użytkownik
**Chcę** oznaczyć zadanie jako wykonane
**Aby** śledzić postęp

**Kryteria Akceptacji:**
- [ ] Checkbox przy zadaniu (lub dropdown ze statusami)
- [ ] Zmiana statusu bez przeładowania strony (AJAX opcjonalnie)
- [ ] Zadania "Done" mogą być ukryte (toggle)
- [ ] Komunikat "Status zaktualizowany"

**Priorytet:** MUST HAVE
**Punkty:** 2
**Status:** To Do

---

### US-023: Edycja i Usuwanie Zadania
**Jako** użytkownik
**Chcę** edytować lub usunąć zadanie
**Aby** zarządzać moją listą rzeczy do zrobienia

**Kryteria Akceptacji:**
- [ ] Przycisk "Edytuj" otwiera formularz edycji
- [ ] Formularz jest wypełniony aktualnymi danymi
- [ ] Przycisk "Usuń" z modalem potwierdzenia
- [ ] Po usunięciu zadanie znika z listy

**Priorytet:** SHOULD HAVE
**Punkty:** 2
**Status:** To Do

---

## Epic 6: Dashboard

### US-024: Dashboard z Podsumowaniem
**Jako** użytkownik
**Chcę** zobaczyć podsumowanie mojej aktywności
**Aby** mieć szybki przegląd sytuacji

**Kryteria Akceptacji:**
- [ ] Kafelki z liczbami:
  - Całkowita liczba kontaktów
  - Kontakty według statusu (Lead, Prospect, Customer)
  - Zadania na dziś
  - Ostatnie interakcje (5 najnowszych)
- [ ] Linki szybkich akcji:
  - Dodaj kontakt
  - Dodaj zadanie
  - Zobacz wszystkie kontakty
- [ ] Wykres/chart (opcjonalnie) - rozkład statusów kontaktów

**Priorytet:** SHOULD HAVE
**Punkty:** 5
**Status:** To Do

---

## Epic 7: AI Assistant (Opcjonalne)

### US-025: Generowanie Podsumowania Kontaktu
**Jako** użytkownik
**Chcę** wygenerować podsumowanie kontaktu przez AI
**Aby** szybko poznać jego sytuację

**Kryteria Akceptacji:**
- [ ] Przycisk "Generuj podsumowanie AI" na stronie kontaktu
- [ ] AI analizuje: notatki, interakcje, zadania
- [ ] Generowane jest podsumowanie (3-5 zdań)
- [ ] Podsumowanie wyświetlane w karcie na stronie
- [ ] Opcja zapisania podsumowania jako notatka
- [ ] Loader podczas generowania

**Priorytet:** COULD HAVE
**Punkty:** 5
**Status:** Backlog

---

### US-026: Sugestia Następnego Kroku
**Jako** użytkownik
**Chcę** otrzymać sugestię następnego kroku
**Aby** wiedzieć jak działać z klientem

**Kryteria Akceptacji:**
- [ ] AI sugeruje akcję na podstawie historii (np. "Skontaktuj się ponownie za tydzień")
- [ ] Sugestia jest konkretna i wykonalna
- [ ] Opcja utworzenia zadania z sugestii (1-click)
- [ ] Wyświetlana pod podsumowaniem

**Priorytet:** COULD HAVE
**Punkty:** 3
**Status:** Backlog

---

## Epic 8: UI/UX

### US-027: Responsywny Design
**Jako** użytkownik mobilny
**Chcę** korzystać z CRM na telefonie
**Aby** mieć dostęp w terenie

**Kryteria Akceptacji:**
- [ ] Layout dostosowuje się do ekranów: mobile, tablet, desktop
- [ ] Nawigacja na mobile jako hamburger menu
- [ ] Tabele przewijalne poziomo na małych ekranach
- [ ] Formularze czytelne na mobile
- [ ] Przyciski dotykowe min. 44x44px

**Priorytet:** SHOULD HAVE
**Punkty:** 5
**Status:** To Do

---

### US-028: Spójny Wygląd
**Jako** użytkownik
**Chcę** korzystać z estetycznego interfejsu
**Aby** przyjemnie pracować

**Kryteria Akceptacji:**
- [ ] Spójna kolorystyka (Bootstrap theme)
- [ ] Ikony Bootstrap Icons
- [ ] Komunikaty success/error w toastach/alerts
- [ ] Przejścia hover na przyciskach
- [ ] Loading spinners przy dłuższych operacjach

**Priorytet:** SHOULD HAVE
**Punkty:** 3
**Status:** To Do

---

## Podsumowanie Priorytetów

### MUST HAVE (MVP)
- Epic 1: Zarządzanie Kontem (US-001 do US-003)
- Epic 2: Zarządzanie Kontaktami (US-005 do US-011)
- Epic 4: Interakcje (US-016, US-017)
- Epic 5: Zadania (US-019, US-020, US-022)

### SHOULD HAVE
- Epic 1: Profil (US-004)
- Epic 3: Firmy (US-012 do US-015)
- Epic 4: Usuwanie interakcji (US-018)
- Epic 5: Edycja zadań (US-021, US-023)
- Epic 6: Dashboard (US-024)
- Epic 8: UX (US-027, US-028)

### COULD HAVE
- Epic 7: AI Assistant (US-025, US-026)

### WON'T HAVE (v1.0)
- Reset hasła przez email
- Eksport/Import CSV
- Powiadomienia email
- API publiczne

---

**Total Story Points:** ~75
**Estimated Duration:** 8-10 dni roboczych
**Team Size:** 1 developer (+ AI Assistant)
