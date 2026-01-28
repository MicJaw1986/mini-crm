# 🚀 Przewodnik po CI/CD i GitHub Actions - Od podstaw

## 🎯 Czym jest CI/CD?

### CI - Continuous Integration (Ciągła Integracja)

**Definicja**: Automatyczne sprawdzanie i testowanie kodu za każdym razem gdy ktoś wprowadza zmiany.

**Jak to działa?**
1. Developer pisze kod i robi commit
2. Wypycha (push) kod do GitHub
3. Automatycznie uruchamiają się testy
4. Jeśli testy przechodzą ✅ - kod jest OK
5. Jeśli testy nie przechodzą ❌ - developer dostaje powiadomienie

**Po co to?**
- Wykrywasz błędy natychmiast (nie po tygodniu!)
- Masz pewność, że nowy kod nie zepsuł starego
- Cały zespół pracuje na działającym kodzie
- Oszczędzasz czas na ręcznym testowaniu

### CD - Continuous Deployment (Ciągłe Wdrażanie)

**Definicja**: Automatyczne wdrażanie (deployment) kodu na serwer, jeśli wszystkie testy przeszły.

**Jak to działa?**
1. Testy przechodzą ✅
2. Automatycznie buduje się aplikacja
3. Automatycznie wdraża się na serwer (np. Heroku, AWS)
4. Użytkownicy mają nową wersję w kilka minut

**Po co to?**
- Szybkie dostarczanie nowych funkcji
- Brak ręcznego wdrażania (mniej błędów)
- Konsystentny proces deployment

## 🤖 Czym jest GitHub Actions?

**GitHub Actions** to darmowy serwis GitHub do automatyzacji zadań.

### Analogia z prawdziwym życiem:

Wyobraź sobie **robota**, który:
1. Czeka aż wypchniesz kod do GitHub
2. Pobiera Twój kod na swój komputer
3. Instaluje Python i wszystkie biblioteki
4. Uruchamia testy
5. Wysyła Ci raport: "Wszystko działa!" lub "Błąd w pliku X"

**To właśnie robi GitHub Actions!**

### Jak to wygląda w praktyce?

```
Ty robisz: git push
↓
GitHub Actions:
  ✓ Pobieranie kodu...
  ✓ Instalacja Python 3.14...
  ✓ pip install -r requirements.txt...
  ✓ Uruchomienie testów...
  ✓ 42/42 testy przeszły!
  ✓ Sprawdzanie jakości kodu...
  ✓ Wszystko OK! ✅
```

## 📋 Kluczowe pojęcia

### 1. Workflow (Przepływ pracy)
**Co to?** Plik YAML, który opisuje co ma się wydarzyć.

**Analogia**: Przepis kulinarny
- Przepis = Workflow
- Kroki przepisu = Jobs
- "Podgrzej piekarnik" = Run tests

**Lokalizacja**: `.github/workflows/nazwa.yml`

### 2. Event (Zdarzenie)
**Co to?** Coś co uruchamia workflow.

**Przykłady**:
- `push` - ktoś wypchnął kod
- `pull_request` - ktoś stworzył PR
- `schedule` - codziennie o 9:00
- `workflow_dispatch` - ręcznie kliknięte

### 3. Job (Zadanie)
**Co to?** Zestaw kroków do wykonania.

**Przykład**: Job "test" składa się z:
- Zainstaluj Python
- Zainstaluj zależności
- Uruchom testy

### 4. Step (Krok)
**Co to?** Pojedyncza operacja.

**Przykłady**:
- `run: python -m pip install Django`
- `run: python manage.py test`

### 5. Runner (Wykonawca)
**Co to?** Serwer, który wykonuje workflow.

**Typy**:
- `ubuntu-latest` - serwer Linux (najczęściej używany)
- `windows-latest` - serwer Windows
- `macos-latest` - serwer macOS

## 🏗️ Struktura pliku Workflow

### Podstawowy szablon:

```yaml
name: Nazwa workflow              # Nazwa wyświetlana w GitHub

on:                               # Kiedy uruchomić?
  push:                           # Przy każdym push
    branches: [ main ]            # Na branchu main
  pull_request:                   # Przy każdym PR
    branches: [ main ]

jobs:                             # Lista zadań
  test:                           # Nazwa joba
    runs-on: ubuntu-latest        # System operacyjny

    steps:                        # Lista kroków
    - uses: actions/checkout@v4   # Pobierz kod

    - name: Setup Python          # Nazwa kroku
      uses: actions/setup-python@v5
      with:
        python-version: '3.14'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test
```

### Wyjaśnienie linijka po linijce:

**`name: CI`**
- Nazwa workflow, która pojawi się w zakładce "Actions"

**`on: push:`**
- Workflow uruchomi się gdy ktoś zrobi `git push`

**`branches: [ main ]`**
- Tylko gdy push jest na branch `main`

**`jobs:`**
- Sekcja z zadaniami do wykonania

**`test:`**
- Nazwa joba (możesz mieć wiele: test, build, deploy)

**`runs-on: ubuntu-latest`**
- Na jakim systemie uruchomić? (Linux Ubuntu)

**`steps:`**
- Lista kroków do wykonania po kolei

**`uses: actions/checkout@v4`**
- Gotowa akcja GitHub - pobiera Twój kod

**`uses: actions/setup-python@v5`**
- Gotowa akcja - instaluje Python

**`with: python-version: '3.14'`**
- Parametr dla akcji - jaka wersja Python?

**`run: |`**
- Uruchom komendy shell (wszystko po `|`)

## 📝 Workflow dla Django - Krok po kroku

### Poziom 1: Podstawowe testy

```yaml
name: Django CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.14'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test
```

**Co to robi?**
1. Pobiera kod z repozytorium
2. Instaluje Python 3.14
3. Instaluje wszystkie biblioteki z requirements.txt
4. Uruchamia testy Django

### Poziom 2: Z coverage (pokrycie testami)

```yaml
name: Django CI with Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.14'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage

    - name: Run tests with coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report
        coverage html

    - name: Upload coverage report
      uses: actions/upload-artifact@v4
      with:
        name: coverage-report
        path: htmlcov/
```

**Nowe elementy**:
- `pip install coverage` - instaluje narzędzie coverage
- `coverage run` - uruchamia testy z pomiarem pokrycia
- `coverage report` - pokazuje % pokrycia
- `actions/upload-artifact` - zapisuje raport HTML

### Poziom 3: Wielowersyjne testowanie (matrix)

```yaml
name: Django CI - Multiple Python versions

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.12', '3.13', '3.14']
        django-version: ['5.0', '5.1']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Django ${{ matrix.django-version }}
      run: |
        pip install Django==${{ matrix.django-version }}
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test
```

**Co to robi?**
Uruchamia testy dla **każdej kombinacji**:
- Python 3.12 + Django 5.0
- Python 3.12 + Django 5.1
- Python 3.13 + Django 5.0
- Python 3.13 + Django 5.1
- Python 3.14 + Django 5.0
- Python 3.14 + Django 5.1

= **6 różnych testów automatycznie!**

### Poziom 4: Pełny workflow produkcyjny

```yaml
name: Django CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.14'

jobs:
  # Job 1: Linting (sprawdzanie jakości kodu)
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install linters
      run: |
        pip install flake8 black isort

    - name: Check code formatting
      run: |
        black --check .
        isort --check-only .

    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  # Job 2: Testy jednostkowe
  test:
    runs-on: ubuntu-latest
    needs: lint  # Uruchom tylko jeśli lint przeszedł

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage

    - name: Run migrations
      run: |
        python manage.py migrate

    - name: Run tests with coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report --fail-under=80
        coverage xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml

  # Job 3: Sprawdzanie bezpieczeństwa
  security:
    runs-on: ubuntu-latest
    needs: lint

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install security tools
      run: |
        pip install safety bandit

    - name: Check for known vulnerabilities
      run: |
        pip install -r requirements.txt
        safety check

    - name: Run bandit security scan
      run: |
        bandit -r . -ll

  # Job 4: Build i deploy (tylko na main)
  deploy:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to production
      run: |
        echo "Deploying to production server..."
        # Tutaj komenda deployment (np. Heroku, AWS)
```

**Co się dzieje?**

1. **Lint Job**: Sprawdza formatowanie kodu
2. **Test Job**: Uruchamia testy (tylko jeśli lint OK)
3. **Security Job**: Skanuje pod kątem podatności
4. **Deploy Job**: Wdraża na produkcję (tylko main branch)

## 🎨 Użyteczne akcje GitHub

### 1. actions/checkout@v4
Pobiera kod z repozytorium.
```yaml
- uses: actions/checkout@v4
```

### 2. actions/setup-python@v5
Instaluje Python.
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.14'
```

### 3. actions/cache@v4
Cachuje zależności (przyspiesza workflow).
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 4. actions/upload-artifact@v4
Zapisuje pliki (np. raporty).
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: htmlcov/
```

### 5. codecov/codecov-action@v4
Wysyła coverage do Codecov.com.
```yaml
- uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
```

## 🔧 Zmienne środowiskowe i sekrety

### Environment Variables (Zmienne środowiskowe)

**Poziom workflow**:
```yaml
env:
  PYTHON_VERSION: '3.14'
  DEBUG: 'False'

jobs:
  test:
    steps:
    - run: echo $PYTHON_VERSION
```

**Poziom job**:
```yaml
jobs:
  test:
    env:
      DATABASE_URL: 'sqlite:///test.db'
    steps:
    - run: python manage.py migrate
```

**Poziom step**:
```yaml
- name: Run command
  env:
    SECRET_KEY: 'test-key'
  run: python manage.py check
```

### Secrets (Tajne klucze)

**Gdzie dodać?**
GitHub → Settings → Secrets and variables → Actions → New repository secret

**Jak użyć?**
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_PASSWORD: ${{ secrets.DB_PASSWORD }}
  run: |
    echo "Deploying with API key..."
```

**Nigdy nie commituj**:
- SECRET_KEY
- DATABASE_PASSWORD
- API_KEYS
- Tokenów dostępu

## 📊 Badge (odznaka) w README

Dodaj ładną odznakę pokazującą status CI:

```markdown
![Django CI](https://github.com/username/repo/workflows/Django%20CI/badge.svg)
```

**Przykład**:
![CI](https://img.shields.io/badge/build-passing-brightgreen)

## 🚦 Status checks i branch protection

### Co to?
GitHub może zablokować merge PR jeśli testy nie przechodzą.

### Jak włączyć?
1. GitHub → Settings → Branches
2. Add rule dla `main`
3. Zaznacz: "Require status checks to pass"
4. Wybierz workflow: `test`

**Efekt**: Nikt nie może zmergować kodu który psuje testy!

## 🎓 Ćwiczenie praktyczne

### Zadanie: Stwórz swój pierwszy workflow

1. Utwórz folder `.github/workflows/`
2. Stwórz plik `django-ci.yml`
3. Skopiuj ten kod:

```yaml
name: My First CI

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
    - name: Say hello
      run: echo "Hello from GitHub Actions!"

    - name: Show date
      run: date
```

4. Zrób commit i push
5. Zobacz w GitHub → Actions

**Gratulacje! Właśnie uruchomiłeś swój pierwszy workflow! 🎉**

## 📚 Kolejne kroki

1. ✅ Zrozum podstawy CI/CD
2. ✅ Stwórz prosty workflow
3. ✅ Dodaj uruchamianie testów
4. ✅ Dodaj coverage
5. ✅ Dodaj linting (flake8, black)
6. ✅ Dodaj security check (safety, bandit)
7. ✅ Skonfiguruj branch protection
8. ✅ Dodaj deployment

## 🔗 Przydatne linki

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

## 💡 Najczęstsze pytania

**Q: Czy GitHub Actions jest darmowy?**
A: Tak, dla repozytoriów publicznych. Private repos mają limit 2000 minut/miesiąc.

**Q: Jak debugować workflow?**
A: Zobacz logi w GitHub → Actions → kliknij na workflow → kliknij na job

**Q: Czy mogę uruchomić workflow lokalnie?**
A: Tak, użyj narzędzia `act`: https://github.com/nektos/act

**Q: Co jeśli workflow trwa zbyt długo?**
A: Użyj cache dla zależności, ogranicz testy do zmienionych plików

---

**Następny krok**: Stwórz plik workflow dla naszego projektu MiniCRM!
