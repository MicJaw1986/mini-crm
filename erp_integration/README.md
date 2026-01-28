# Moduł integracji ERP

Uniwersalny moduł do integracji MiniCRM z systemami ERP (Comarch ERP XL, SAP, własne API).

## 📋 Spis treści

1. [Architektura](#architektura)
2. [Szybki start](#szybki-start)
3. [Konfiguracja](#konfiguracja)
4. [Implementacja endpointów](#implementacja-endpointów)
5. [Użycie w widokach](#użycie-w-widokach)
6. [Modele cache](#modele-cache)
7. [Testowanie](#testowanie)
8. [FAQ](#faq)

---

## Architektura

### Komponenty

```
erp_integration/
├── services/
│   ├── base_client.py       # Abstrakcyjny interfejs (kontrakt)
│   └── comarch_client.py    # Implementacja dla Comarch ERP XL
├── models.py                # Modele cache (opcjonalne)
├── views.py                 # Widoki do wyświetlania danych ERP
├── urls.py                  # Routing
└── templates/               # Szablony HTML
```

### Przepływ danych

```
1. LIVE MODE (bez cache):
   CRM → ComarchERPClient → API ERP → Response → Widok → Szablon

2. CACHE MODE (z synchronizacją):
   CRM → ComarchERPClient → API ERP → Cache (ERPOrder, ERPInvoice) → Widok
   [Background task co X minut synchronizuje cache]
```

---

## Szybki start

### 1. Konfiguracja API

Edytuj `mini_crm/settings.py` lub stwórz plik `.env`:

```python
# .env lub bezpośrednio w settings.py
COMARCH_API_URL=https://twoj-erp.com/api
COMARCH_API_KEY=twoj_api_key_tutaj
ERP_INTEGRATION_ENABLED=True
```

### 2. Wypełnij endpointy w `comarch_client.py`

Otwórz plik `erp_integration/services/comarch_client.py` i znajdź sekcje z `# TODO`.

**Przykład - Zamówienia klienta:**

```python
def get_customer_orders(self, customer_code: str, ...) -> List[Dict]:
    # TODO: Wpisz prawdziwy endpoint
    endpoint = f"api/v1/customers/{customer_code}/orders"
    # Według Twojej dokumentacji Postman

    params = {
        'limit': limit,
        # Dodaj inne parametry według dokumentacji
    }

    data = self._request('GET', endpoint, params=params)

    # TODO: Mapuj pola z response API na standardowy format
    return [
        {
            'order_id': item['Id'],              # Dopasuj do prawdziwej nazwy pola
            'order_number': item['OrderNumber'],
            'order_date': item['Date'],
            # ... reszta pól
        }
        for item in data.get('results', [])
    ]
```

### 3. Test połączenia

```bash
./venv/Scripts/python manage.py shell
```

```python
from erp_integration.services.comarch_client import ComarchERPClient

client = ComarchERPClient()

# Test podstawowego połączenia
print(client.get_api_info())

# Test pobrania klienta
customer = client.get_customer('KH001')
print(customer)

# Test zamówień
orders = client.get_customer_orders('KH001', limit=5)
for order in orders:
    print(f"{order['order_number']} - {order['total_gross']} PLN")
```

---

## Konfiguracja

### Zmienne środowiskowe (.env)

```bash
# === API ERP ===
COMARCH_API_URL=https://your-server.com/api
COMARCH_API_KEY=your_api_key_here
# LUB jeśli używasz Basic Auth:
COMARCH_API_USER=api_user
COMARCH_API_PASSWORD=api_password

# === Opcje ===
ERP_INTEGRATION_ENABLED=True      # Włącz integrację
ERP_CACHE_ENABLED=False           # False = zawsze live data
COMARCH_TIMEOUT=30                # Timeout HTTP w sekundach
```

### Autoryzacja

`comarch_client.py` obsługuje kilka metod autoryzacji. Edytuj metodę `_get_headers()`:

**1. Bearer Token (API Key)**
```python
def _get_headers(self):
    headers = {
        'Authorization': f'Bearer {self.api_key}',
        'Content-Type': 'application/json',
    }
    return headers
```

**2. Custom API Key Header**
```python
headers = {
    'X-API-Key': self.api_key,
    'Content-Type': 'application/json',
}
```

**3. Basic Auth**
```python
# W metodzie _request():
response = requests.request(
    method=method,
    url=url,
    headers=self._get_headers(),
    auth=(self.api_user, self.api_password),  # <-- Dodaj to
    params=params,
    json=data,
    timeout=self.timeout,
)
```

---

## Implementacja endpointów

### Proces wypełniania

Dla każdej metody w `comarch_client.py`:

1. **Znajdź endpoint w dokumentacji Postman**
2. **Wpisz URL endpointu**
3. **Dopasuj parametry**
4. **Zmapuj pola response**

### Przykład kompletny - Faktury

**1. Z dokumentacji Postman:**
```
GET /api/v1/invoices?customer_id=123&type=FS
Response:
{
  "data": [
    {
      "invoice_id": "12345",
      "number": "FS/2024/001",
      "type": "FS",
      "issue_date": "2024-01-15",
      "total_amount": 12300.00,
      ...
    }
  ]
}
```

**2. Implementacja:**
```python
def get_customer_invoices(
    self,
    customer_code: str,
    invoice_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:

    # Endpoint z dokumentacji
    endpoint = "api/v1/invoices"

    # Parametry według dokumentacji
    params = {
        'customer_id': customer_code,  # Nazwa parametru z dokumentacji
        'limit': limit,
    }

    if invoice_type:
        params['type'] = invoice_type

    if date_from:
        params['date_from'] = date_from.strftime('%Y-%m-%d')  # Format daty z dokumentacji

    # Wykonaj request
    response_data = self._request('GET', endpoint, params=params)

    # Pobierz listę faktur (może być response_data['data'], response_data['results'], etc.)
    items = response_data.get('data', [])

    # Mapuj pola na standardowy format
    return [
        {
            # Lewa strona = standardowy format (nie zmieniaj!)
            # Prawa strona = nazwy pól z API (dopasuj do dokumentacji!)
            'invoice_id': item.get('invoice_id', ''),
            'invoice_number': item.get('number', ''),
            'invoice_type': item.get('type', 'FS'),
            'invoice_date': item.get('issue_date', ''),
            'sale_date': item.get('sale_date', ''),
            'due_date': item.get('due_date', ''),
            'customer_code': customer_code,
            'customer_name': item.get('customer_name', ''),
            'total_net': float(item.get('net_amount', 0)),
            'total_gross': float(item.get('total_amount', 0)),
            'currency': item.get('currency', 'PLN'),
            'payment_status': item.get('payment_status', 'unpaid'),
            'paid_amount': float(item.get('paid', 0)),
            'remaining_amount': float(item.get('remaining', 0)),
            'items': self._parse_invoice_items(item.get('items', [])),
        }
        for item in items[:limit]
    ]
```

### Checklist implementacji

Dla każdego endpointu wypełnij:

- [ ] `get_customer()` - dane kontrahenta
- [ ] `search_customers()` - wyszukiwanie
- [ ] `get_customer_orders()` - zamówienia
- [ ] `get_order_detail()` - szczegóły zamówienia
- [ ] `get_customer_invoices()` - faktury
- [ ] `get_invoice_detail()` - szczegóły faktury
- [ ] `get_customer_delivery_notes()` - dokumenty WZ
- [ ] `get_customer_payments()` - płatności
- [ ] `get_customer_summary()` - podsumowanie

---

## Użycie w widokach

### Przykład widoku Django

```python
# contacts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from contacts.models import Company
from erp_integration.services.comarch_client import ComarchERPClient


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    # Dane ERP (jeśli skonfigurowane)
    erp_data = None
    if settings.ERP_INTEGRATION_ENABLED and company.erp_customer_code:
        try:
            client = ComarchERPClient()

            # Pobierz dane z ERP
            erp_data = {
                'summary': client.get_customer_summary(company.erp_customer_code),
                'orders': client.get_customer_orders(company.erp_customer_code, limit=5),
                'invoices': client.get_customer_invoices(company.erp_customer_code, limit=5),
            }
        except Exception as e:
            print(f"ERP error: {e}")
            erp_data = None

    context = {
        'company': company,
        'erp_data': erp_data,
    }

    return render(request, 'contacts/company_detail.html', context)
```

### W szablonie

```html
<!-- contacts/templates/contacts/company_detail.html -->

{% if erp_data %}
<div class="card mt-3">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0"><i class="bi bi-database"></i> Dane z ERP</h5>
    </div>
    <div class="card-body">
        <!-- Podsumowanie -->
        <div class="row">
            <div class="col-md-3">
                <h6>Zamówienia</h6>
                <h3>{{ erp_data.summary.total_orders }}</h3>
                <small>{{ erp_data.summary.total_orders_value|floatformat:2 }} PLN</small>
            </div>
            <div class="col-md-3">
                <h6>Faktury nieopłacone</h6>
                <h3 class="text-warning">{{ erp_data.summary.unpaid_invoices }}</h3>
                <small>{{ erp_data.summary.unpaid_amount|floatformat:2 }} PLN</small>
            </div>
            <div class="col-md-3">
                <h6>Zaległe faktury</h6>
                <h3 class="text-danger">{{ erp_data.summary.overdue_invoices }}</h3>
                <small>{{ erp_data.summary.overdue_amount|floatformat:2 }} PLN</small>
            </div>
        </div>

        <!-- Ostatnie zamówienia -->
        <h6 class="mt-4">Ostatnie zamówienia</h6>
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>Numer</th>
                    <th>Data</th>
                    <th>Wartość</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for order in erp_data.orders %}
                <tr>
                    <td>{{ order.order_number }}</td>
                    <td>{{ order.order_date }}</td>
                    <td>{{ order.total_gross|floatformat:2 }} {{ order.currency }}</td>
                    <td><span class="badge bg-info">{{ order.status }}</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Ostatnie faktury -->
        <h6 class="mt-4">Ostatnie faktury</h6>
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>Numer</th>
                    <th>Data</th>
                    <th>Wartość</th>
                    <th>Status płatności</th>
                </tr>
            </thead>
            <tbody>
                {% for invoice in erp_data.invoices %}
                <tr>
                    <td>{{ invoice.invoice_number }}</td>
                    <td>{{ invoice.invoice_date }}</td>
                    <td>{{ invoice.total_gross|floatformat:2 }} {{ invoice.currency }}</td>
                    <td>
                        {% if invoice.payment_status == 'paid' %}
                        <span class="badge bg-success">Opłacona</span>
                        {% elif invoice.payment_status == 'overdue' %}
                        <span class="badge bg-danger">Zaległa</span>
                        {% else %}
                        <span class="badge bg-warning">Nieopłacona</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endif %}
```

---

## Modele cache

### Kiedy używać cache?

**Używaj cache jeśli:**
- API ERP jest wolne (>1s response time)
- Są limity requestów (rate limiting)
- Chcesz historycznych danych offline
- Dashboard wymaga agregacji wielu zapytań

**Nie używaj cache jeśli:**
- API ERP jest szybkie (<200ms)
- Zawsze potrzebujesz live data
- Masz mało użytkowników/requestów

### Włączenie cache

```python
# settings.py
ERP_CACHE_ENABLED = True
```

### Synchronizacja cache

Stwórz management command lub Celery task:

```python
# erp_integration/management/commands/sync_erp.py
from django.core.management.base import BaseCommand
from contacts.models import Company
from erp_integration.models import ERPOrder, ERPInvoice
from erp_integration.services.comarch_client import ComarchERPClient


class Command(BaseCommand):
    help = 'Synchronizuj dane z ERP'

    def handle(self, *args, **options):
        client = ComarchERPClient()

        companies_with_erp = Company.objects.exclude(erp_customer_code='')

        for company in companies_with_erp:
            self.stdout.write(f"Syncing {company.name}...")

            # Pobierz zamówienia z API
            orders = client.get_customer_orders(company.erp_customer_code, limit=100)

            # Zapisz/update w cache
            for order_data in orders:
                ERPOrder.objects.update_or_create(
                    order_id=order_data['order_id'],
                    defaults={
                        'company': company,
                        'order_number': order_data['order_number'],
                        'order_date': order_data['order_date'],
                        'total_net': order_data['total_net'],
                        'total_gross': order_data['total_gross'],
                        'currency': order_data['currency'],
                        'status': order_data['status'],
                        'raw_data': order_data,  # Backup pełnych danych
                    }
                )

            # To samo dla faktur, WZ, etc.

        self.stdout.write(self.style.SUCCESS('Sync completed!'))
```

Uruchom:
```bash
./venv/Scripts/python manage.py sync_erp
```

Lub dodaj do crontab/Task Scheduler (Windows):
```
0 */6 * * * cd /path/to/MiniCrm && ./venv/Scripts/python manage.py sync_erp
```

---

## Testowanie

### Test w Django shell

```bash
./venv/Scripts/python manage.py shell
```

```python
from erp_integration.services.comarch_client import ComarchERPClient
from datetime import date, timedelta

client = ComarchERPClient()

# Test 1: Info o API
print(client.get_api_info())

# Test 2: Pobierz klienta
customer = client.get_customer('KH001')
if customer:
    print(f"Klient: {customer['name']}")
    print(f"NIP: {customer['nip']}")
    print(f"Saldo: {customer['balance']} PLN")

# Test 3: Zamówienia z ostatnich 30 dni
date_from = date.today() - timedelta(days=30)
orders = client.get_customer_orders('KH001', date_from=date_from, limit=10)
print(f"Znaleziono {len(orders)} zamówień")
for order in orders:
    print(f"  {order['order_number']} - {order['total_gross']} {order['currency']}")

# Test 4: Faktury nieopłacone
invoices = client.get_customer_invoices('KH001', limit=20)
unpaid = [inv for inv in invoices if inv['payment_status'] in ['unpaid', 'overdue']]
print(f"Nieopłacone faktury: {len(unpaid)}")

# Test 5: Podsumowanie
summary = client.get_customer_summary('KH001')
print(f"Podsumowanie: {summary}")
```

### Obsługa błędów

Client automatycznie loguje błędy do console. Możesz dodać własne logowanie:

```python
import logging

logger = logging.getLogger(__name__)

try:
    orders = client.get_customer_orders('KH001')
except requests.exceptions.HTTPError as e:
    logger.error(f"HTTP error: {e}")
    # Pokaż komunikat użytkownikowi
except requests.exceptions.Timeout:
    logger.error("ERP timeout")
except Exception as e:
    logger.error(f"ERP error: {e}")
```

---

## FAQ

### Q: Czy muszę wypełnić wszystkie metody?

Nie! Zacznij od tych które Ci potrzebne:
1. `get_customer()` - dane klienta
2. `get_customer_orders()` - zamówienia
3. `get_customer_invoices()` - faktury

Resztę możesz dodać później.

### Q: Co jeśli moje API ma inną strukturę JSON?

W `comarch_client.py` mapujesz pola API na standardowy format. Przykład:

```python
# API zwraca:
{
  "OrderID": "123",
  "OrderNo": "ZAM/001",
  "TotalWithVAT": 1230.00
}

# Mapujesz na standardowy format:
{
  'order_id': item['OrderID'],           # Dopasuj nazwę pola
  'order_number': item['OrderNo'],
  'total_gross': float(item['TotalWithVAT']),
}
```

### Q: Jak dodać support dla innego ERP (nie Comarch)?

Stwórz nowy plik np. `sap_client.py`:

```python
from .base_client import BaseERPClient

class SAPERPClient(BaseERPClient):
    def __init__(self):
        self.base_url = settings.SAP_API_URL
        # ...

    def get_customer(self, customer_code):
        # Implementacja dla SAP
        pass
```

Potem w widokach:
```python
from erp_integration.services.sap_client import SAPERPClient
client = SAPERPClient()
```

### Q: Czy to działa z Comarch ERP Optima?

Tak, jeśli Optima ma API REST/SOAP. Proces jest identyczny - tylko endpointy będą inne.

### Q: Wydajność - ile requestów na stronę?

**Bez cache:** 1 request na każde wywołanie (np. company detail = 3 requesty dla orders/invoices/summary)

**Z cache:** 0 requestów w runtime (dane z bazy), synchronizacja w tle co X godzin

**Optymalizacja:**
- Użyj cache dla dashboardu (wiele agregacji)
- Live data dla szczegółów (zawsze aktualne)
- Cache dla raportów historycznych

### Q: Bezpieczeństwo - czy API credentials są bezpieczne?

**Best practices:**
1. Użyj zmiennych środowiskowych (.env)
2. Nigdy nie commituj credentials do git
3. W produkcji użyj secrets manager (AWS Secrets, Azure Key Vault)
4. Ogranicz uprawnienia API user w ERP (read-only)

```python
# .env (dodaj do .gitignore!)
COMARCH_API_KEY=secret_key_here
```

---

## Następne kroki

1. **Wypełnij endpointy** w `comarch_client.py`
2. **Testuj w shell** każdą metodę
3. **Dodaj widget ERP** do `company_detail.html`
4. **Opcjonalnie**: Skonfiguruj cache i synchronizację

**Potrzebujesz pomocy?** Daj znać które endpointy już masz z dokumentacji Postman - mogę pomóc z mapowaniem!
