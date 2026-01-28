# 📚 Przykłady Workflow GitHub Actions

Ten dokument zawiera gotowe do użycia przykłady workflow dla różnych scenariuszy.

## 📋 Spis treści

1. [Prosty workflow - tylko testy](#1-prosty-workflow---tylko-testy)
2. [Workflow z coverage](#2-workflow-z-coverage)
3. [Matrix testing - wiele wersji](#3-matrix-testing---wiele-wersji)
4. [Scheduled workflow - codzienne testy](#4-scheduled-workflow---codzienne-testy)
5. [Deployment na Heroku](#5-deployment-na-heroku)
6. [Notification na Slack](#6-notification-na-slack)
7. [Dependency updates (Dependabot)](#7-dependency-updates-dependabot)

---

## 1. Prosty workflow - tylko testy

**Plik**: `.github/workflows/simple-test.yml`

```yaml
name: Simple Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test
```

**Kiedy używać?**
- Małe projekty
- Szybkie sprawdzenie czy testy przechodzą
- Nauka GitHub Actions

---

## 2. Workflow z coverage

**Plik**: `.github/workflows/test-with-coverage.yml`

```yaml
name: Tests with Coverage

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage

    - name: Run tests with coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report --show-missing

    - name: Generate coverage badge
      run: |
        coverage report | grep TOTAL | awk '{print $NF}' > coverage.txt
        cat coverage.txt

    - name: Upload coverage report
      uses: actions/upload-artifact@v4
      with:
        name: coverage-report
        path: htmlcov/
```

**Dodatki**:
- Pokazuje które linie NIE są testowane (`--show-missing`)
- Generuje raport HTML
- Zapisuje raport jako artifact

---

## 3. Matrix testing - wiele wersji

**Plik**: `.github/workflows/matrix-test.yml`

```yaml
name: Matrix Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false  # Nie zatrzymuj innych jeśli jeden fail
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
        django-version: ['4.2', '5.0', '5.1']

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

    - name: Show environment info
      run: |
        python --version
        pip show django
```

**Co to testuje?**
- 3 systemy operacyjne × 3 wersje Python × 3 wersje Django = **27 kombinacji!**
- Automatycznie wykrywa problemy kompatybilności

**Uwaga**: Matrix testing zużywa więcej minut GitHub Actions!

---

## 4. Scheduled workflow - codzienne testy

**Plik**: `.github/workflows/nightly.yml`

```yaml
name: Nightly Tests

on:
  schedule:
    # Uruchom codziennie o 2:00 UTC (3:00 CET w zimie, 4:00 CEST w lecie)
    - cron: '0 2 * * *'
  workflow_dispatch:  # Pozwala uruchomić ręcznie

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run full test suite
      run: |
        python manage.py test --verbosity=2

    - name: Send notification on failure
      if: failure()
      run: |
        echo "Nightly tests failed! Check logs."
        # Tutaj możesz dodać wysyłanie emaila/Slack
```

**Cron syntax**:
```
┌───────────── minuta (0 - 59)
│ ┌───────────── godzina (0 - 23)
│ │ ┌───────────── dzień miesiąca (1 - 31)
│ │ │ ┌───────────── miesiąc (1 - 12)
│ │ │ │ ┌───────────── dzień tygodnia (0 - 6) (0=niedziela)
│ │ │ │ │
* * * * *
```

**Przykłady**:
- `0 2 * * *` - codziennie o 2:00
- `0 2 * * 1` - każdy poniedziałek o 2:00
- `0 */4 * * *` - co 4 godziny
- `0 0 1 * *` - pierwszego dnia każdego miesiąca

---

## 5. Deployment na Heroku

**Plik**: `.github/workflows/deploy-heroku.yml`

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]  # Deploy tylko z main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test

  deploy:
    needs: test  # Uruchom tylko jeśli testy przeszły
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.13.15
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: 'twoja-aplikacja-crm'
        heroku_email: 'twoj-email@example.com'

    - name: Run migrations on Heroku
      run: |
        heroku run python manage.py migrate --app twoja-aplikacja-crm
      env:
        HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
```

**Jak skonfigurować?**

1. Uzyskaj Heroku API key:
   ```bash
   heroku auth:token
   ```

2. Dodaj secret w GitHub:
   - Settings → Secrets → New repository secret
   - Name: `HEROKU_API_KEY`
   - Value: [Twój token]

3. Zmień w workflow:
   - `twoja-aplikacja-crm` → nazwa Twojej app na Heroku
   - `twoj-email@example.com` → Twój email Heroku

---

## 6. Notification na Slack

**Plik**: `.github/workflows/slack-notify.yml`

```yaml
name: Tests with Slack Notification

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test

    # Wyślij powiadomienie na Slack jeśli SUKCES
    - name: Slack Notification - Success
      if: success()
      uses: rtCamp/action-slack-notify@v2
      env:
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_CHANNEL: '#ci-notifications'
        SLACK_COLOR: 'good'
        SLACK_TITLE: 'Tests Passed ✅'
        SLACK_MESSAGE: 'All tests passed successfully!'

    # Wyślij powiadomienie na Slack jeśli BŁĄD
    - name: Slack Notification - Failure
      if: failure()
      uses: rtCamp/action-slack-notify@v2
      env:
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_CHANNEL: '#ci-notifications'
        SLACK_COLOR: 'danger'
        SLACK_TITLE: 'Tests Failed ❌'
        SLACK_MESSAGE: 'Tests failed! Check logs.'
```

**Jak skonfigurować Slack?**

1. Utwórz Incoming Webhook w Slack:
   - https://api.slack.com/messaging/webhooks
   - Wybierz kanał (np. `#ci-notifications`)
   - Skopiuj Webhook URL

2. Dodaj secret w GitHub:
   - Settings → Secrets → New repository secret
   - Name: `SLACK_WEBHOOK`
   - Value: [Webhook URL]

---

## 7. Dependency updates (Dependabot)

**Plik**: `.github/dependabot.yml`

```yaml
# Automatyczne update'y zależności
version: 2
updates:
  # Update'y Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"  # Sprawdzaj co tydzień
      day: "monday"       # W poniedziałki
      time: "09:00"       # O 9:00
    open-pull-requests-limit: 5  # Max 5 PR jednocześnie
    labels:
      - "dependencies"
      - "python"
    reviewers:
      - "twoja-nazwa-uzytkownika"  # Przypisz do review
    assignees:
      - "twoja-nazwa-uzytkownika"

  # Update'y GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    labels:
      - "dependencies"
      - "github-actions"
```

**Co to robi?**
- Automatycznie sprawdza czy są nowe wersje bibliotek
- Tworzy Pull Request z update'ami
- Uruchamia testy dla nowej wersji
- Jeśli testy przechodzą - możesz zmergować

**Przykładowy PR od Dependabot**:
```
Bump Django from 5.0.1 to 5.0.2

Bumps Django from 5.0.1 to 5.0.2.
- Release notes
- Changelog
- Commits

This PR updates Django to fix security vulnerabilities.
```

---

## 🎨 Kombinacje workflow

### Produkcyjny setup - wszystko razem

**Plik**: `.github/workflows/production.yml`

```yaml
name: Production Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.12'

jobs:
  # Job 1: Testy
  test:
    runs-on: ubuntu-latest
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
    - name: Run tests with coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report --fail-under=80
        coverage xml
    - name: Upload to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml

  # Job 2: Linting
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    - name: Lint
      run: |
        pip install flake8 black isort
        black --check .
        isort --check-only .
        flake8 .

  # Job 3: Security
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Security scan
      run: |
        pip install safety bandit
        pip install -r requirements.txt
        safety check
        bandit -r . -ll

  # Job 4: Deploy (tylko na main po przejściu testów)
  deploy:
    needs: [test, lint, security]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
    - name: Notify success
      if: success()
      run: |
        echo "Deployment successful!"
```

---

## 💡 Pro Tips

### Tip 1: Używaj cache dla szybszych buildów

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Efekt**: Build 2-3x szybszy!

### Tip 2: Conditional steps (warunkowe kroki)

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'  # Tylko na main
  run: ./deploy.sh

- name: Send notification
  if: failure()  # Tylko jeśli coś nie przeszło
  run: echo "Build failed!"

- name: Cleanup
  if: always()  # Zawsze, nawet jeśli były błędy
  run: rm -rf temp/
```

### Tip 3: Reusable workflows

Stwórz `.github/workflows/reusable-test.yml`:

```yaml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
    - name: Run tests
      run: python manage.py test
```

Użyj w innym workflow:

```yaml
jobs:
  test-python-312:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.12'
```

---

## 🔗 Przydatne linki

- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Gotowe szablony!** Skopiuj, dostosuj i używaj! 🚀
