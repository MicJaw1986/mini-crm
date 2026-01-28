# 🎯 Jak skonfigurować GitHub Actions dla MiniCRM - Krok po kroku

## 📋 Czego się nauczysz?

W tym przewodniku dowiesz się:
1. Jak przygotować projekt do CI/CD
2. Jak dodać workflow GitHub Actions
3. Jak sprawdzić czy działa
4. Jak interpretować wyniki
5. Jak naprawić błędy

## ✅ Wymagania

- [x] Konto GitHub
- [x] Repozytorium projektu MiniCRM na GitHub
- [x] Kod lokalnie (git clone)
- [x] Napisane testy (mamy 42 testy!)

## 🚀 Krok 1: Przygotowanie projektu

### 1.1. Sprawdź czy testy działają lokalnie

**Dlaczego?** Jeśli testy nie działają u Ciebie, nie będą działać na GitHub Actions!

```bash
python manage.py test
```

**Oczekiwany wynik**:
```
Ran 42 tests in XX.XXXs
OK
```

Jeśli widzisz błędy - napraw je PRZED przejściem dalej!

### 1.2. Sprawdź requirements.txt

**Dlaczego?** GitHub Actions instaluje zależności z tego pliku.

Upewnij się że masz wszystkie potrzebne biblioteki:

```txt
Django>=5.0,<6.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

**Sprawdź**:
```bash
pip freeze | grep Django
pip freeze | grep pillow
```

### 1.3. Dodaj coverage do requirements (opcjonalnie)

Jeśli chcesz mierzyć pokrycie testami:

```bash
pip install coverage
pip freeze | grep coverage >> requirements.txt
```

## 🎬 Krok 2: Dodanie workflow do projektu

### 2.1. Utwórz strukturę folderów

```bash
mkdir -p .github/workflows
```

**Objaśnienie**:
- `.github/` - folder specjalny GitHub (ukryty)
- `workflows/` - tutaj przechowujemy pliki YAML z workflow

### 2.2. Skopiuj plik workflow

Już mamy plik: `.github/workflows/django-ci.yml`

**Sprawdź czy istnieje**:
```bash
ls .github/workflows/
```

Powinieneś zobaczyć: `django-ci.yml`

### 2.3. Zrozum strukturę pliku

Otwórz `.github/workflows/django-ci.yml` i przeanalizuj sekcje:

```yaml
name: Django CI          # Nazwa workflow

on:                      # Kiedy uruchomić?
  push:
    branches: [ main ]   # Na jakich branchach?

jobs:                    # Co wykonać?
  test:                  # Nazwa joba
    runs-on: ubuntu-latest
    steps:               # Kroki
    - uses: actions/checkout@v4
    - name: Install
      run: pip install -r requirements.txt
```

## 📤 Krok 3: Wypchanie kodu na GitHub

### 3.1. Sprawdź status git

```bash
git status
```

Powinieneś zobaczyć:
```
.github/workflows/django-ci.yml
```

### 3.2. Dodaj pliki do commita

```bash
git add .github/workflows/django-ci.yml
git add docs/cicd-guide.md
git add docs/github-actions-setup.md
```

### 3.3. Stwórz commit

```bash
git commit -m "feat: dodaj GitHub Actions CI/CD workflow

- Workflow uruchamia testy automatycznie
- Sprawdza pokrycie testami (coverage)
- Wykonuje linting (flake8)
- Skanuje bezpieczeństwo (safety, bandit)
- Dodano dokumentację CI/CD

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### 3.4. Wypchnij kod

```bash
git push origin main
```

**UWAGA**: Jeśli używasz innego brancha (np. `develop`), zmień `main` na swoją nazwę.

## 🔍 Krok 4: Sprawdzenie workflow na GitHub

### 4.1. Przejdź do zakładki Actions

1. Otwórz przeglądarkę
2. Wejdź na GitHub.com
3. Otwórz swoje repozytorium
4. Kliknij zakładkę **"Actions"** (u góry)

### 4.2. Zobacz uruchomiony workflow

Powinieneś zobaczyć:
```
Django CI
feat: dodaj GitHub Actions CI/CD workflow
● in progress (pomarańczowa kropka)
```

Lub jeśli już skończył:
```
✓ Django CI (zielony ptaszek)
✗ Django CI (czerwony krzyżyk - jeśli błąd)
```

### 4.3. Kliknij na workflow

Zobaczysz 3 joby:
```
✓ test       (2m 15s)
✓ lint       (45s)
✓ security   (1m 30s)
```

### 4.4. Sprawdź logi

Kliknij na job np. "test" → Zobaczysz wszystkie kroki:

```
✓ Checkout code (1s)
✓ Set up Python 3.14 (5s)
✓ Cache pip dependencies (2s)
✓ Install dependencies (45s)
✓ Check Django configuration (2s)
✓ Run tests with coverage (30s)
  Ran 42 tests in 28.543s
  OK
✓ Check coverage threshold (1s)
  Coverage: 85%
✓ Upload coverage report (5s)
```

## 🎉 Krok 5: Interpretacja wyników

### ✅ Sukces (zielony ptaszek)

**Co to znaczy?**
- Wszystkie testy przeszły
- Coverage ≥ 70%
- Kod jest zgodny z PEP 8
- Brak znanych podatności

**Co zrobić?**
- Nic! Możesz mergować kod
- Możesz tworzyć Pull Request

### ❌ Błąd (czerwony krzyżyk)

**Co to znaczy?**
- Przynajmniej jeden test nie przeszedł
- Lub coverage < 70%
- Lub błędy lintingu
- Lub problemy bezpieczeństwa

**Co zrobić?**
1. Kliknij na czerwony job
2. Zobacz który krok się nie powiódł
3. Przeczytaj logi błędów
4. Napraw błąd lokalnie
5. Zrób commit i push ponownie

### Przykładowe błędy i jak je naprawić:

#### Błąd: "Test failed"
```
FAILED tests/test_models.py::test_contact_creation
AssertionError: Expected 'Jan Kowalski' but got 'JanKowalski'
```

**Rozwiązanie**:
1. Uruchom test lokalnie: `python manage.py test tests.test_models`
2. Napraw kod
3. Sprawdź czy działa: `python manage.py test`
4. Commit i push

#### Błąd: "Coverage below 70%"
```
Coverage: 65%
```

**Rozwiązanie**:
1. Uruchom lokalnie: `coverage run --source='.' manage.py test`
2. Zobacz raport: `coverage report`
3. Zobacz co nie jest pokryte: `coverage html` → otwórz `htmlcov/index.html`
4. Napisz brakujące testy
5. Sprawdź coverage ponownie

#### Błąd: "Flake8 linting errors"
```
./views.py:45:80: E501 line too long (95 > 79 characters)
```

**Rozwiązanie**:
1. Zainstaluj flake8: `pip install flake8`
2. Uruchom: `flake8 .`
3. Napraw błędy (skróć linie, popraw formatowanie)
4. Sprawdź: `flake8 .`
5. Commit i push

## 🏆 Krok 6: Badge w README

### 6.1. Dodaj badge do README.md

Otwórz `README.md` i dodaj na górze:

```markdown
# MiniCRM

![Django CI](https://github.com/TWOJA-NAZWA/MiniCrm/workflows/Django%20CI/badge.svg)

System CRM do zarządzania kontaktami, zadaniami i interakcjami.
```

**Zamień**:
- `TWOJA-NAZWA` → Twoja nazwa użytkownika GitHub
- `MiniCrm` → Nazwa repozytorium (jeśli inna)

### 6.2. Zobacz efekt

Po pushu zobaczysz ładną odznakę:

![CI passing](https://img.shields.io/badge/build-passing-brightgreen)

Jeśli testy nie przeszły:

![CI failing](https://img.shields.io/badge/build-failing-red)

## 🛡️ Krok 7: Branch protection (opcjonalnie)

### Co to daje?
Nikt (nawet Ty!) nie może zmergować kodu który nie przeszedł testów.

### Jak włączyć?

1. GitHub → Twoje repo → **Settings**
2. Sidebar → **Branches**
3. Kliknij **"Add rule"**
4. Branch name pattern: `main`
5. Zaznacz:
   - ☑ Require status checks to pass before merging
   - ☑ Require branches to be up to date before merging
   - ☑ Status checks that are required:
     - `test`
     - `lint`
     - `security`
6. Kliknij **"Create"**

**Efekt**: Przycisk "Merge" będzie zablokowany dopóki CI nie przejdzie!

## 📊 Krok 8: Pobieranie raportów coverage

### 8.1. Gdzie znaleźć?

1. GitHub → Actions
2. Kliknij na konkretny workflow run
3. Scroll na dół → **Artifacts**
4. Kliknij **"coverage-report"** → Pobierz ZIP

### 8.2. Otwórz raport

1. Rozpakuj ZIP
2. Otwórz `index.html` w przeglądarce
3. Zobacz:
   - % pokrycia dla każdego pliku
   - Które linie kodu NIE są testowane (czerwone)
   - Które linie SĄ testowane (zielone)

### 8.3. Popraw pokrycie

Dla linii czerwonych (nie testowanych):
1. Napisz test sprawdzający tę linię
2. Uruchom: `coverage run --source='.' manage.py test`
3. Sprawdź: `coverage report`
4. Powtarzaj aż coverage ≥ 70%

## 🚨 Najczęstsze problemy

### Problem: "Workflow nie uruchomił się"

**Przyczyny**:
1. Plik nie jest w `.github/workflows/`
2. Plik nie ma rozszerzenia `.yml` lub `.yaml`
3. Push był na inny branch (workflow działa tylko na `main`)

**Rozwiązanie**:
```bash
ls .github/workflows/  # Sprawdź czy plik istnieje
git branch             # Sprawdź na jakim branchu jesteś
```

### Problem: "Python 3.14 not found"

**Przyczyna**: GitHub Actions nie ma jeszcze Python 3.14

**Rozwiązanie**: Zmień w workflow:
```yaml
python-version: '3.12'  # Zamiast 3.14
```

### Problem: "Module not found"

**Przyczyna**: Brak biblioteki w `requirements.txt`

**Rozwiązanie**:
1. Dodaj do `requirements.txt`
2. Commit i push

### Problem: "Database error"

**Przyczyna**: Testy próbują użyć prawdziwej bazy

**Rozwiązanie**: Sprawdź `settings.py` - w testach powinno być:
```python
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
```

## 🎓 Zadania praktyczne

### Zadanie 1: Dodaj swój pierwszy workflow
- [ ] Stwórz `.github/workflows/hello.yml`
- [ ] Dodaj prosty step: `run: echo "Hello GitHub Actions!"`
- [ ] Push i zobacz w Actions

### Zadanie 2: Napraw celowo zepsuty test
- [ ] Zmień assert w teście tak żeby nie przeszedł
- [ ] Push
- [ ] Zobacz czerwony krzyżyk w GitHub
- [ ] Napraw
- [ ] Push i zobacz zielony ptaszek

### Zadanie 3: Popraw coverage
- [ ] Uruchom `coverage report` lokalnie
- [ ] Znajdź plik z najniższym %
- [ ] Napisz test dla nie pokrytych linii
- [ ] Sprawdź czy coverage wzrósł

## 📚 Następne kroki

Po skonfigurowaniu CI/CD możesz:

1. ✅ Dodać więcej jobów (np. deployment)
2. ✅ Skonfigurować notifications (email, Slack)
3. ✅ Dodać matrix testing (różne wersje Python/Django)
4. ✅ Integrować z Codecov.io (wizualizacja coverage)
5. ✅ Dodać automatyczne security updates (Dependabot)

## 🔗 Przydatne komendy

```bash
# Lokalnie - uruchom testy
python manage.py test

# Lokalnie - coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Lokalnie - linting
pip install flake8
flake8 .

# Lokalnie - security
pip install safety bandit
safety check
bandit -r .

# Git - status
git status
git log --oneline

# Git - push
git add .
git commit -m "commit message"
git push origin main
```

## 💡 Pro Tips

1. **Używaj cache** - przyspiesza workflow o 50%
2. **Testuj lokalnie PRZED push** - oszczędzasz czas
3. **Czytaj logi** - zawsze mówią co jest nie tak
4. **Branch protection** - wymusza dobre praktyki
5. **Badge w README** - pokazuje status projektu

---

**Gratulacje!** 🎉 Właśnie skonfigurowałeś profesjonalny pipeline CI/CD!

Każdy push będzie automatycznie testowany. Nigdy więcej nie zepsujesz produkcji!
