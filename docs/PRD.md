# Product Requirements Document (PRD)
## Mini CRM - System Zarządzania Relacjami z Klientami

**Wersja:** 1.0.0
**Data:** 2026-01-17
**Autor:** Projekt zaliczeniowy

---

## 1. Przegląd Produktu

### 1.1 Cel Biznesowy
Mini CRM to webowa aplikacja do zarządzania kontaktami biznesowymi, firmami i interakcjami z klientami. System umożliwia śledzenie historii komunikacji, zarządzanie zadaniami oraz wykorzystanie sztucznej inteligencji do generowania podsumowań i sugestii działań.

### 1.2 Grupa Docelowa
- Freelancerzy i samozatrudnieni
- Małe zespoły sprzedażowe (do 10 osób)
- Konsultanci biznesowi
- Account managerowie

### 1.3 Problem Biznesowy
Małe zespoły często korzystają z arkuszy kalkulacyjnych lub notatek do zarządzania kontaktami, co prowadzi do:
- Utraty informacji o klientach
- Braku historii interakcji
- Nieefektywnego planowania follow-upów
- Trudności w śledzeniu statusu leadów

---

## 2. Zakres Funkcjonalny

### 2.1 Wymagania Obowiązkowe (MVP)

#### 2.1.1 Moduł Autentykacji (Accounts)
- **REQ-001:** Rejestracja nowego użytkownika z walidacją email
- **REQ-002:** Logowanie użytkownika (email/username + hasło)
- **REQ-003:** Wylogowanie użytkownika
- **REQ-004:** Widok profilu użytkownika
- **REQ-005:** Ochrona widoków - dostęp tylko dla zalogowanych użytkowników

#### 2.1.2 Moduł Kontaktów (Contacts)
- **REQ-006:** Lista wszystkich kontaktów użytkownika
- **REQ-007:** Dodawanie nowego kontaktu (imię, nazwisko, email, telefon, pozycja, firma)
- **REQ-008:** Edycja istniejącego kontaktu
- **REQ-009:** Usuwanie kontaktu (z potwierdzeniem)
- **REQ-010:** Wyszukiwanie kontaktów po imieniu/nazwisku
- **REQ-011:** Filtrowanie kontaktów po statusie (Lead, Prospect, Customer, Churned)
- **REQ-012:** Widok szczegółów kontaktu z historią interakcji

#### 2.1.3 Moduł Firm (Companies)
- **REQ-013:** Lista firm
- **REQ-014:** Dodawanie nowej firmy (nazwa, branża, strona www, adres)
- **REQ-015:** Edycja firmy
- **REQ-016:** Usuwanie firmy
- **REQ-017:** Przypisanie kontaktu do firmy
- **REQ-018:** Widok szczegółów firmy z listą przypisanych kontaktów

#### 2.1.4 Moduł Interakcji (Interactions)
- **REQ-019:** Dodawanie notatki do kontaktu
- **REQ-020:** Rejestrowanie typu interakcji (notatka, telefon, email, spotkanie)
- **REQ-021:** Wyświetlanie timeline'u interakcji przy kontakcie (chronologicznie)
- **REQ-022:** Usuwanie interakcji

#### 2.1.5 Moduł Zadań (Tasks)
- **REQ-023:** Dodawanie zadania powiązanego z kontaktem
- **REQ-024:** Ustawianie terminu wykonania zadania
- **REQ-025:** Zmiana statusu zadania (To Do, In Progress, Done)
- **REQ-026:** Lista zadań zaplanowanych na dziś (dashboard)
- **REQ-027:** Edycja i usuwanie zadań

#### 2.1.6 Dashboard
- **REQ-028:** Strona główna z podsumowaniem:
  - Liczba kontaktów według statusu
  - Zadania na dziś
  - Ostatnie interakcje
  - Statystyki podstawowe

### 2.2 Wymagania Opcjonalne (Future Enhancements)

#### 2.2.1 Moduł AI (AI Assistant)
- **REQ-029:** Generowanie podsumowania kontaktu na podstawie notatek i interakcji
- **REQ-030:** Sugestia następnego kroku działania (np. "Skontaktuj się ponownie za tydzień")
- **REQ-031:** Analiza sentymentu interakcji (pozytywne/neutralne/negatywne)

#### 2.2.2 Dodatkowe Funkcje
- **REQ-032:** Reset hasła przez email
- **REQ-033:** Eksport kontaktów do CSV
- **REQ-034:** Import kontaktów z CSV
- **REQ-035:** Powiadomienia email o nadchodzących zadaniach

---

## 3. Wymagania Niefunkcjonalne

### 3.1 Bezpieczeństwo
- **NFR-001:** Hashowanie haseł (Django PBKDF2)
- **NFR-002:** Ochrona CSRF dla wszystkich formularzy
- **NFR-003:** Walidacja danych wejściowych
- **NFR-004:** Izolacja danych użytkowników (jeden użytkownik nie widzi danych innego)

### 3.2 Wydajność
- **NFR-005:** Czas ładowania strony < 2s (na standardowym połączeniu)
- **NFR-006:** Obsługa do 1000 kontaktów na użytkownika bez spadku wydajności

### 3.3 Użyteczność
- **NFR-007:** Responsywny design (mobile-friendly)
- **NFR-008:** Intuicyjny interfejs użytkownika
- **NFR-009:** Spójny wygląd wizualny (Bootstrap 5)

### 3.4 Dostępność
- **NFR-010:** Aplikacja dostępna 24/7 (po wdrożeniu na hosting)
- **NFR-011:** Wsparcie dla przeglądarek: Chrome, Firefox, Safari, Edge (najnowsze 2 wersje)

### 3.5 Testowalność
- **NFR-012:** Pokrycie testami jednostkowymi min. 70%
- **NFR-013:** Minimum 1 test E2E weryfikujący pełną ścieżkę użytkownika
- **NFR-014:** Testy CI/CD w GitHub Actions

---

## 4. User Stories

### Epic 1: Zarządzanie Kontem
- **US-001:** Jako nowy użytkownik chcę się zarejestrować, aby móc korzystać z systemu
- **US-002:** Jako użytkownik chcę się zalogować, aby uzyskać dostęp do moich danych
- **US-003:** Jako użytkownik chcę się wylogować, aby zabezpieczyć swoje konto

### Epic 2: Zarządzanie Kontaktami
- **US-004:** Jako użytkownik chcę dodać nowy kontakt, aby przechowywać informacje o kliencie
- **US-005:** Jako użytkownik chcę zobaczyć listę wszystkich moich kontaktów
- **US-006:** Jako użytkownik chcę edytować kontakt, aby zaktualizować jego dane
- **US-007:** Jako użytkownik chcę usunąć kontakt, który nie jest już aktualny
- **US-008:** Jako użytkownik chcę wyszukać kontakt po nazwisku, aby szybko go znaleźć
- **US-009:** Jako użytkownik chcę filtrować kontakty po statusie, aby zobaczyć np. tylko aktywnych klientów

### Epic 3: Zarządzanie Firmami
- **US-010:** Jako użytkownik chcę dodać firmę, aby grupować kontakty według organizacji
- **US-011:** Jako użytkownik chcę przypisać kontakt do firmy

### Epic 4: Interakcje i Historia
- **US-012:** Jako użytkownik chcę dodać notatkę do kontaktu, aby zapamiętać szczegóły rozmowy
- **US-013:** Jako użytkownik chcę zobaczyć historię wszystkich interakcji z danym kontaktem
- **US-014:** Jako użytkownik chcę oznaczyć typ interakcji (telefon/email/spotkanie)

### Epic 5: Zarządzanie Zadaniami
- **US-015:** Jako użytkownik chcę utworzyć zadanie powiązane z kontaktem, aby nie zapomnieć o follow-upie
- **US-016:** Jako użytkownik chcę zobaczyć listę zadań na dziś
- **US-017:** Jako użytkownik chcę oznaczyć zadanie jako wykonane

### Epic 6: Dashboard i Przegląd
- **US-018:** Jako użytkownik chcę zobaczyć podsumowanie moich kontaktów i zadań po zalogowaniu

### Epic 7: AI Assistant (Opcjonalne)
- **US-019:** Jako użytkownik chcę wygenerować podsumowanie kontaktu, aby szybko poznać jego sytuację
- **US-020:** Jako użytkownik chcę otrzymać sugestię następnego kroku w relacji z klientem

---

## 5. Modele Danych

### 5.1 User (Django built-in)
- Standardowy model użytkownika Django
- Rozszerzony o profil (opcjonalnie)

### 5.2 Company
```
- id: AutoField (PK)
- user: ForeignKey -> User
- name: CharField(200)
- website: URLField
- industry: CharField(100)
- address: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 5.3 Contact
```
- id: AutoField (PK)
- user: ForeignKey -> User
- company: ForeignKey -> Company (nullable)
- first_name: CharField(100)
- last_name: CharField(100)
- email: EmailField
- phone: CharField(20)
- position: CharField(100)
- status: CharField(choices: lead/prospect/customer/churned)
- notes: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 5.4 Interaction
```
- id: AutoField (PK)
- contact: ForeignKey -> Contact
- user: ForeignKey -> User
- interaction_type: CharField(choices: note/call/email/meeting)
- content: TextField
- created_at: DateTimeField
```

### 5.5 Task
```
- id: AutoField (PK)
- contact: ForeignKey -> Contact (nullable)
- user: ForeignKey -> User
- title: CharField(200)
- description: TextField
- status: CharField(choices: todo/in_progress/done)
- due_date: DateField (nullable)
- created_at: DateTimeField
- updated_at: DateTimeField
```

---

## 6. Interfejs Użytkownika

### 6.1 Strony
1. **Strona główna / Landing** - prezentacja produktu (opcjonalna)
2. **Logowanie** - formularz logowania
3. **Rejestracja** - formularz rejestracji
4. **Dashboard** - podsumowanie po zalogowaniu
5. **Lista kontaktów** - tabela z wyszukiwaniem i filtrami
6. **Szczegóły kontaktu** - timeline interakcji, zadania, przyciski akcji
7. **Formularz kontaktu** - dodawanie/edycja
8. **Lista firm** - tabela firm
9. **Szczegóły firmy** - lista przypisanych kontaktów
10. **Formularz firmy** - dodawanie/edycja
11. **Lista zadań** - wszystkie zadania z filtrowaniem
12. **Profil użytkownika**

### 6.2 Nawigacja
- Górna belka: Logo, Kontakty, Firmy, Zadania, Profil, Wyloguj
- Sidebar na dashboardzie z szybkimi akcjami

---

## 7. Kryteria Sukcesu

### 7.1 Funkcjonalne
- ✅ Użytkownik może się zarejestrować i zalogować
- ✅ Użytkownik może dodać, edytować, usunąć kontakt
- ✅ Użytkownik może dodać notatkę i zadanie do kontaktu
- ✅ Użytkownik widzi tylko swoje dane (izolacja)
- ✅ Dashboard wyświetla aktualne statystyki

### 7.2 Techniczne
- ✅ Wszystkie testy przechodzą (unit + E2E)
- ✅ CI/CD pipeline działa poprawnie
- ✅ Aplikacja zdeployowana pod publicznym URL
- ✅ Dokumentacja kompletna (PRD, Tech Spec, README)

### 7.3 Zaliczeniowe
- ✅ Mechanizm kontroli dostępu ✓
- ✅ CRUD dla danych ✓
- ✅ Logika biznesowa (statusy, zadania) ✓
- ✅ Dokumentacja ✓
- ✅ Test E2E ✓
- ✅ Pipeline CI/CD ✓

---

## 8. Out of Scope (v1.0)

Następujące funkcje **NIE** będą zaimplementowane w pierwszej wersji:
- ❌ System uprawnień wieloużytkownikowych (tylko owner widzi swoje dane)
- ❌ Współdzielenie kontaktów między użytkownikami
- ❌ Integracje z zewnętrznymi systemami (Gmail, Calendar, etc.)
- ❌ Zaawansowane raporty i analytics
- ❌ Mobile app (native)
- ❌ API publiczne
- ❌ System powiadomień push

---

## 9. Timeline i Kamienie Milowe

### Milestone 1: Dokumentacja i Setup (Dzień 1)
- PRD, Tech Spec, User Stories
- Inicjalizacja projektu Django
- Konfiguracja Git i GitHub

### Milestone 2: Autentykacja (Dzień 2)
- Moduł accounts z logowaniem i rejestracją
- Podstawowe szablony i nawigacja

### Milestone 3: CRUD Kontaktów i Firm (Dzień 3-4)
- Modele Contact i Company
- Pełny CRUD z widokami i szablonami
- Wyszukiwanie i filtrowanie

### Milestone 4: Interakcje i Zadania (Dzień 5)
- Moduł interactions
- Moduł tasks
- Timeline na stronie kontaktu

### Milestone 5: Dashboard i UI (Dzień 6-7)
- Dashboard z podsumowaniem
- Bootstrap styling
- Responsywność

### Milestone 6: Testy i CI/CD (Dzień 8)
- Testy jednostkowe
- Test E2E Playwright
- GitHub Actions workflow

### Milestone 7: Deployment (Dzień 9-10)
- Konfiguracja produkcyjna
- Deploy na Railway/Render
- Finalne poprawki

### Milestone 8: AI Integration (Opcjonalne)
- Integracja z Claude API
- Generowanie podsumowań
- Sugestie działań

---

## 10. Ryzyka i Mitigacje

| Ryzyko | Prawdopodobieństwo | Wpływ | Mitigacja |
|--------|-------------------|-------|-----------|
| Brak czasu na AI | Średnie | Niski | AI jest opcjonalne, focus na CRUD |
| Problemy z deploymentem | Niskie | Średni | Railway/Render mają dobre docs |
| Testy E2E niestabilne | Średnie | Średni | Użyj prostych scenariuszy |
| Zmiany w wymaganiach | Niskie | Wysoki | PRD zatwierdzony na starcie |

---

## 11. Glossary

- **CRM** - Customer Relationship Management (Zarządzanie Relacjami z Klientami)
- **Lead** - Potencjalny klient w fazie początkowej
- **Prospect** - Kwalifikowany lead, zainteresowany ofertą
- **Customer** - Aktywny klient
- **Churned** - Klient, który zrezygnował
- **Interaction** - Każda forma kontaktu z klientem
- **Timeline** - Chronologiczna historia interakcji
- **Follow-up** - Kolejna akcja kontaktowa
- **CRUD** - Create, Read, Update, Delete

---

**Zatwierdzenie:**
- [ ] Product Owner
- [ ] Tech Lead
- [ ] Stakeholder

**Historia zmian:**
- 2026-01-17: v1.0.0 - Inicjalna wersja dokumentu
