# 🚀 Quick Start - Integracja ERP

## Krok 1: Konfiguracja podstawowa (5 min)

### A. Dodaj credentials do .env

```bash
# Otwórz plik .env lub stwórz go jeśli nie istnieje
notepad .env
```

Dodaj:
```bash
COMARCH_API_URL=https://twoj-serwer-erp.com/api
COMARCH_API_KEY=twoj_api_key_tutaj
ERP_INTEGRATION_ENABLED=True
```

### B. Test połączenia

```bash
# Uruchom Django shell
./venv/Scripts/python manage.py shell
```

```python
from erp_integration.services.comarch_client import ComarchERPClient

# Stwórz instancję clienta
client = ComarchERPClient()

# Test 1: Info o połączeniu
print(client.get_api_info())
# Powinno zwrócić informacje o API

# Test 2: Sprawdź czy połączenie działa
if client.test_connection():
    print("✅ Połączenie z ERP działa!")
else:
    print("❌ Błąd połączenia - sprawdź credentials w .env")
```

---

## Krok 2: Wypełnij PIERWSZY endpoint (10 min)

Otwórz `erp_integration/services/comarch_client.py`

### Znajdź metodę `get_customer()`

**Z dokumentacji Postman skopiuj:**
1. Endpoint URL (np. `api/v1/customers/{code}`)
2. Nazwy pól w response JSON

**Przykład:**

Jeśli dokumentacja pokazuje:
```json
GET /api/v1/kontrahenci/KH001
Response:
{
  "Id": "KH001",
  "Nazwa": "Firma ABC",
  "NIP": "1234567890",
  "Email": "kontakt@abc.pl",
  "Saldo": -15000.00
}
```

Wypełnij w kodzie:
```python
def get_customer(self, customer_code: str) -> Optional[Dict[str, Any]]:
    # 1. Wpisz endpoint z dokumentacji
    endpoint = f"api/v1/kontrahenci/{customer_code}"

    try:
        data = self._request('GET', endpoint)

        # 2. Zmapuj pola (lewa strona = standard, prawa = z API)
        return {
            'code': data.get('Id', customer_code),
            'name': data.get('Nazwa', ''),
            'nip': data.get('NIP', ''),
            'address': data.get('Adres', ''),  # jeśli jest w API
            'email': data.get('Email', ''),
            'phone': data.get('Telefon', ''),  # jeśli jest w API
            'payment_terms': data.get('TerminPlatnosci', ''),
            'credit_limit': float(data.get('LimitKredytowy', 0)),
            'balance': float(data.get('Saldo', 0)),
        }

    except Exception as e:
        print(f"Error fetching customer {customer_code}: {e}")
        return None
```

### Testuj

```python
from erp_integration.services.comarch_client import ComarchERPClient

client = ComarchERPClient()

# Użyj prawdziwego kodu klienta z Twojego ERP
customer = client.get_customer('KH001')  # Zmień KH001 na prawdziwy kod

if customer:
    print(f"✅ Działa! Klient: {customer['name']}")
    print(f"   NIP: {customer['nip']}")
    print(f"   Saldo: {customer['balance']} PLN")
else:
    print("❌ Nie udało się pobrać klienta")
```

---

## Krok 3: Wypełnij zamówienia (15 min)

### Znajdź metodę `get_customer_orders()`

**Z dokumentacji Postman:**
```
GET /api/v1/zamowienia?customer_code=KH001&limit=10
```

**Wypełnij:**
```python
def get_customer_orders(
    self,
    customer_code: str,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:

    # Wpisz endpoint
    endpoint = "api/v1/zamowienia"  # LUB f"api/v1/customers/{customer_code}/orders"

    # Parametry według dokumentacji
    params = {
        'customer_code': customer_code,  # Sprawdź nazwę parametru w dokumentacji
        'limit': limit,
    }

    # Dodaj daty jeśli są w API
    if date_from:
        params['date_from'] = date_from.isoformat()  # LUB .strftime('%Y-%m-%d')

    if date_to:
        params['date_to'] = date_to.isoformat()

    try:
        data = self._request('GET', endpoint, params=params)

        # Sprawdź w dokumentacji jak nazywa się lista wyników
        items = data if isinstance(data, list) else data.get('results', [])
        # Może być: data['data'], data['results'], data['items'], lub bezpośrednio lista

        # Zmapuj każde zamówienie
        return [
            {
                'order_id': item.get('Id', ''),           # Dopasuj do nazw z API
                'order_number': item.get('Numer', ''),
                'order_date': item.get('Data', ''),
                'customer_code': customer_code,
                'customer_name': item.get('NazwaKontrahenta', ''),
                'total_net': float(item.get('WartoscNetto', 0)),
                'total_gross': float(item.get('WartoscBrutto', 0)),
                'currency': item.get('Waluta', 'PLN'),
                'status': item.get('Status', 'unknown'),
                'delivery_date': item.get('DataRealizacji', ''),
                'items': [],  # Na razie pusta lista, możesz dodać później
            }
            for item in items[:limit]
        ]

    except Exception as e:
        print(f"Error fetching orders: {e}")
        return []
```

### Testuj

```python
from erp_integration.services.comarch_client import ComarchERPClient
from datetime import date, timedelta

client = ComarchERPClient()

# Zamówienia z ostatnich 30 dni
date_from = date.today() - timedelta(days=30)
orders = client.get_customer_orders('KH001', date_from=date_from, limit=5)

if orders:
    print(f"✅ Znaleziono {len(orders)} zamówień:")
    for order in orders:
        print(f"   {order['order_number']} - {order['total_gross']} {order['currency']}")
else:
    print("❌ Brak zamówień lub błąd")
```

---

## Krok 4: Dodaj widget ERP do Company Detail (10 min)

### Edytuj widok

Otwórz `contacts/views.py`, znajdź `company_detail` i dodaj:

```python
from django.conf import settings
from erp_integration.services.comarch_client import ComarchERPClient

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    contacts = company.contacts.all().order_by('last_name')

    # === DODAJ TO ===
    erp_data = None
    if settings.ERP_INTEGRATION_ENABLED and company.erp_customer_code:
        try:
            client = ComarchERPClient()
            erp_data = {
                'customer': client.get_customer(company.erp_customer_code),
                'orders': client.get_customer_orders(company.erp_customer_code, limit=5),
                # Dodasz faktury później
            }
        except Exception as e:
            print(f"ERP error: {e}")
            erp_data = None
    # === KONIEC DODAWANIA ===

    context = {
        'company': company,
        'contacts': contacts,
        'erp_data': erp_data,  # === DODAJ DO CONTEXT ===
    }

    return render(request, 'contacts/company_detail.html', context)
```

### Edytuj szablon

Otwórz `contacts/templates/contacts/company_detail.html`, dodaj przed końcem:

```html
<!-- Na końcu przed {% endblock %} -->

{% if erp_data %}
<div class="card mt-4">
    <div class="card-header bg-info text-white">
        <h5 class="mb-0">
            <i class="bi bi-database"></i> Dane z ERP
            <small class="float-end">Kod: {{ company.erp_customer_code }}</small>
        </h5>
    </div>
    <div class="card-body">
        <!-- Dane klienta -->
        {% if erp_data.customer %}
        <div class="row mb-3">
            <div class="col-md-4">
                <strong>Saldo:</strong>
                <span class="{% if erp_data.customer.balance < 0 %}text-danger{% else %}text-success{% endif %}">
                    {{ erp_data.customer.balance|floatformat:2 }} PLN
                </span>
            </div>
            <div class="col-md-4">
                <strong>Limit kredytu:</strong>
                {{ erp_data.customer.credit_limit|floatformat:2 }} PLN
            </div>
            <div class="col-md-4">
                <strong>Termin płatności:</strong>
                {{ erp_data.customer.payment_terms }}
            </div>
        </div>
        {% endif %}

        <!-- Ostatnie zamówienia -->
        <h6 class="mt-3">Ostatnie zamówienia</h6>
        {% if erp_data.orders %}
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>Numer</th>
                    <th>Data</th>
                    <th class="text-end">Wartość brutto</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for order in erp_data.orders %}
                <tr>
                    <td>{{ order.order_number }}</td>
                    <td>{{ order.order_date }}</td>
                    <td class="text-end">{{ order.total_gross|floatformat:2 }} {{ order.currency }}</td>
                    <td><span class="badge bg-info">{{ order.status }}</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p class="text-muted">Brak zamówień</p>
        {% endif %}
    </div>
</div>
{% endif %}
```

### Testuj

1. Otwórz firmę w CRM
2. Edytuj firmę i dodaj **Kod kontrahenta w ERP** (np. `KH001`)
3. Zapisz
4. Odśwież stronę szczegółów firmy
5. Powinien pojawić się widget z danymi ERP!

---

## Krok 5: Dodaj faktury (15 min)

Analogicznie wypełnij `get_customer_invoices()` w `comarch_client.py`

Dodaj do widoku:
```python
erp_data = {
    'customer': client.get_customer(company.erp_customer_code),
    'orders': client.get_customer_orders(company.erp_customer_code, limit=5),
    'invoices': client.get_customer_invoices(company.erp_customer_code, limit=5),  # DODAJ
}
```

Dodaj do szablonu:
```html
<!-- Faktury -->
<h6 class="mt-4">Ostatnie faktury</h6>
{% if erp_data.invoices %}
<table class="table table-sm">
    <thead>
        <tr>
            <th>Numer</th>
            <th>Typ</th>
            <th>Data</th>
            <th>Termin</th>
            <th class="text-end">Wartość</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for inv in erp_data.invoices %}
        <tr>
            <td>{{ inv.invoice_number }}</td>
            <td><span class="badge bg-secondary">{{ inv.invoice_type }}</span></td>
            <td>{{ inv.invoice_date }}</td>
            <td>{{ inv.due_date }}</td>
            <td class="text-end">{{ inv.total_gross|floatformat:2 }} {{ inv.currency }}</td>
            <td>
                {% if inv.payment_status == 'paid' %}
                <span class="badge bg-success">Opłacona</span>
                {% elif inv.payment_status == 'overdue' %}
                <span class="badge bg-danger">Zaległa</span>
                {% else %}
                <span class="badge bg-warning">Nieopłacona</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p class="text-muted">Brak faktur</p>
{% endif %}
```

---

## Krok 6: Obsługa błędów i loading states

### Dodaj graceful degradation

```python
# W widoku
erp_data = None
erp_error = None

if settings.ERP_INTEGRATION_ENABLED and company.erp_customer_code:
    try:
        client = ComarchERPClient()
        erp_data = {
            'customer': client.get_customer(company.erp_customer_code),
            'orders': client.get_customer_orders(company.erp_customer_code, limit=5),
            'invoices': client.get_customer_invoices(company.erp_customer_code, limit=5),
        }
    except requests.exceptions.Timeout:
        erp_error = "Timeout połączenia z ERP. Spróbuj ponownie później."
    except requests.exceptions.HTTPError as e:
        erp_error = f"Błąd API ERP: {e.response.status_code}"
    except Exception as e:
        erp_error = "Błąd pobierania danych z ERP"
        print(f"ERP error details: {e}")

context = {
    'company': company,
    'contacts': contacts,
    'erp_data': erp_data,
    'erp_error': erp_error,  # DODAJ
}
```

### W szablonie

```html
{% if erp_error %}
<div class="alert alert-warning">
    <i class="bi bi-exclamation-triangle"></i> {{ erp_error }}
</div>
{% elif erp_data %}
<!-- Widget ERP -->
{% endif %}
```

---

## Częste problemy

### 1. ImportError: No module named 'requests'

```bash
./venv/Scripts/pip install requests
```

### 2. ValueError: COMARCH_API_URL nie jest skonfigurowany

Sprawdź `.env`:
```bash
COMARCH_API_URL=https://twoj-serwer.com/api  # Musi być wypełnione!
```

### 3. HTTP 401 Unauthorized

Sprawdź credentials w `.env`:
```bash
COMARCH_API_KEY=twoj_klucz  # Sprawdź czy poprawny
```

### 4. HTTP 404 Not Found

Endpoint nieprawidłowy - sprawdź w dokumentacji Postman dokładną ścieżkę.

### 5. KeyError przy mapowaniu pól

Sprawdź nazwy pól w response. Dodaj `print(data)` przed mapowaniem:
```python
data = self._request('GET', endpoint)
print(data)  # Zobacz strukturę response
```

---

## Co dalej?

- [ ] Wypełnij pozostałe metody (WZ, płatności)
- [ ] Dodaj widget ERP do dashboardu
- [ ] Zaimplementuj cache jeśli API jest wolne
- [ ] Dodaj admin panel dla konfiguracji

**Potrzebujesz pomocy?** Zajrzyj do `README.md` lub daj znać!
