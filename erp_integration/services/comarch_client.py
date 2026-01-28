"""
Klient API dla Comarch ERP XL

INSTRUKCJA UŻYCIA:
1. Wypełnij metody API endpoints w sekcjach oznaczonych # TODO
2. Skonfiguruj settings.py (COMARCH_API_URL, COMARCH_API_KEY, etc.)
3. Test connection: python manage.py shell -> from erp_integration.services.comarch_client import ComarchERPClient -> client = ComarchERPClient() -> client.test_connection()
"""

import requests
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from django.conf import settings
from .base_client import BaseERPClient


class ComarchERPClient(BaseERPClient):
    """
    Klient API dla Comarch ERP XL

    Konfiguracja w settings.py:
        COMARCH_API_URL = 'https://your-erp-server.com/api'
        COMARCH_API_KEY = 'your-api-key'
        COMARCH_API_USER = 'api_user'  # opcjonalnie
        COMARCH_API_PASSWORD = 'password'  # opcjonalnie
        COMARCH_TIMEOUT = 30  # timeout w sekundach
    """

    def __init__(self):
        self.base_url = getattr(settings, 'COMARCH_API_URL', '')
        self.api_key = getattr(settings, 'COMARCH_API_KEY', '')
        self.api_user = getattr(settings, 'COMARCH_API_USER', '')
        self.api_password = getattr(settings, 'COMARCH_API_PASSWORD', '')
        self.timeout = getattr(settings, 'COMARCH_TIMEOUT', 30)

        if not self.base_url:
            raise ValueError("COMARCH_API_URL nie jest skonfigurowany w settings.py")

    def _get_headers(self) -> Dict[str, str]:
        """
        Przygotuj nagłówki HTTP dla requestów

        TODO: Dostosuj do systemu autoryzacji Twojego ERP
        - API Key w header
        - Basic Auth
        - Bearer Token
        - Custom header
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # Opcja 1: API Key w header
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
            # LUB
            # headers['X-API-Key'] = self.api_key

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Any:
        """
        Uniwersalna metoda do wykonywania requestów HTTP

        Args:
            method: GET, POST, PUT, DELETE
            endpoint: endpoint API (bez base_url)
            params: parametry URL (query string)
            data: dane do wysłania (JSON body)

        Returns:
            Response JSON lub None
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                params=params,
                json=data,
                timeout=self.timeout,
                # Opcjonalnie - jeśli używasz Basic Auth:
                # auth=(self.api_user, self.api_password) if self.api_user else None
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            # Logowanie błędów HTTP (401, 403, 404, 500, etc.)
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text if e.response else 'No response'}")
            raise

        except requests.exceptions.Timeout:
            print(f"Timeout connecting to {url}")
            raise

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise

    # ========== KONTRAHENCI (CUSTOMERS) ==========

    def get_customer(self, customer_code: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz dane kontrahenta

        TODO: Wypełnij endpoint i mapowanie pól
        """
        # TODO: Wpisz prawdziwy endpoint z dokumentacji Postman
        endpoint = f"customers/{customer_code}"
        # Przykład: endpoint = f"api/v1/kontrahenci/{customer_code}"

        try:
            data = self._request('GET', endpoint)

            # TODO: Mapuj pola z API na standardowy format
            # data może mieć strukturę specyficzną dla Comarch
            # Poniżej przykładowe mapowanie - dostosuj do rzeczywistej struktury

            return {
                'code': data.get('Kod', customer_code),
                'name': data.get('Nazwa', ''),
                'nip': data.get('NIP', ''),
                'address': data.get('Adres', ''),
                'email': data.get('Email', ''),
                'phone': data.get('Telefon', ''),
                'payment_terms': data.get('TerminPlatnosci', ''),
                'credit_limit': float(data.get('LimitKredytowy', 0)),
                'balance': float(data.get('Saldo', 0)),
            }

        except Exception as e:
            print(f"Error fetching customer {customer_code}: {e}")
            return None

    def search_customers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Wyszukaj kontrahentów

        TODO: Wypełnij endpoint i parametry wyszukiwania
        """
        # TODO: Wpisz endpoint do wyszukiwania
        endpoint = "customers"
        # Przykład: endpoint = "api/v1/kontrahenci/search"

        params = {
            'search': query,  # TODO: Dostosuj nazwę parametru
            'limit': limit,
            # 'offset': 0,  # dla paginacji
        }

        try:
            data = self._request('GET', endpoint, params=params)

            # TODO: Dostosuj do struktury response
            # Może być: data['results'], data['items'], lub bezpośrednio lista
            items = data if isinstance(data, list) else data.get('results', [])

            return [
                {
                    'code': item.get('Kod', ''),
                    'name': item.get('Nazwa', ''),
                    'nip': item.get('NIP', ''),
                    'address': item.get('Adres', ''),
                    'email': item.get('Email', ''),
                    'phone': item.get('Telefon', ''),
                    'payment_terms': item.get('TerminPlatnosci', ''),
                    'credit_limit': float(item.get('LimitKredytowy', 0)),
                    'balance': float(item.get('Saldo', 0)),
                }
                for item in items[:limit]
            ]

        except Exception as e:
            print(f"Error searching customers: {e}")
            return []

    # ========== ZAMÓWIENIA (ORDERS) ==========

    def get_customer_orders(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz zamówienia klienta

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"customers/{customer_code}/orders"
        # Przykład: endpoint = f"api/v1/zamowienia"

        params = {
            'customer_code': customer_code,  # TODO: może nie być potrzebne jeśli w URL
            'limit': limit,
        }

        if date_from:
            params['date_from'] = date_from.isoformat()  # TODO: dostosuj format daty

        if date_to:
            params['date_to'] = date_to.isoformat()

        try:
            data = self._request('GET', endpoint, params=params)
            items = data if isinstance(data, list) else data.get('results', [])

            return [
                {
                    'order_id': item.get('Id', ''),
                    'order_number': item.get('Numer', ''),
                    'order_date': item.get('DataZamowienia', ''),
                    'customer_code': customer_code,
                    'customer_name': item.get('NazwaKontrahenta', ''),
                    'total_net': float(item.get('WartoscNetto', 0)),
                    'total_gross': float(item.get('WartoscBrutto', 0)),
                    'currency': item.get('Waluta', 'PLN'),
                    'status': item.get('Status', 'unknown'),
                    'delivery_date': item.get('DataRealizacji', ''),
                    'items': self._parse_order_items(item.get('Pozycje', [])),
                }
                for item in items[:limit]
            ]

        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def _parse_order_items(self, items: List[Dict]) -> List[Dict]:
        """Helper do parsowania pozycji zamówienia"""
        return [
            {
                'product_code': item.get('KodTowaru', ''),
                'product_name': item.get('NazwaTowaru', ''),
                'quantity': float(item.get('Ilosc', 0)),
                'unit': item.get('Jednostka', 'szt'),
                'price_net': float(item.get('CenaNetto', 0)),
                'total_net': float(item.get('WartoscNetto', 0)),
            }
            for item in items
        ]

    def get_order_detail(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz szczegóły zamówienia

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"orders/{order_id}"

        try:
            data = self._request('GET', endpoint)

            return {
                'order_id': data.get('Id', order_id),
                'order_number': data.get('Numer', ''),
                'order_date': data.get('DataZamowienia', ''),
                'customer_code': data.get('KodKontrahenta', ''),
                'customer_name': data.get('NazwaKontrahenta', ''),
                'total_net': float(data.get('WartoscNetto', 0)),
                'total_gross': float(data.get('WartoscBrutto', 0)),
                'currency': data.get('Waluta', 'PLN'),
                'status': data.get('Status', 'unknown'),
                'delivery_date': data.get('DataRealizacji', ''),
                'items': self._parse_order_items(data.get('Pozycje', [])),
            }

        except Exception as e:
            print(f"Error fetching order {order_id}: {e}")
            return None

    # ========== FAKTURY (INVOICES) ==========

    def get_customer_invoices(
        self,
        customer_code: str,
        invoice_type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz faktury klienta

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"customers/{customer_code}/invoices"

        params = {
            'customer_code': customer_code,
            'limit': limit,
        }

        if invoice_type:
            params['type'] = invoice_type  # TODO: dostosuj nazwę parametru

        if date_from:
            params['date_from'] = date_from.isoformat()

        if date_to:
            params['date_to'] = date_to.isoformat()

        try:
            data = self._request('GET', endpoint, params=params)
            items = data if isinstance(data, list) else data.get('results', [])

            return [
                {
                    'invoice_id': item.get('Id', ''),
                    'invoice_number': item.get('Numer', ''),
                    'invoice_type': item.get('TypDokumentu', 'FS'),
                    'invoice_date': item.get('DataWystawienia', ''),
                    'sale_date': item.get('DataSprzedazy', ''),
                    'due_date': item.get('TerminPlatnosci', ''),
                    'customer_code': customer_code,
                    'customer_name': item.get('NazwaKontrahenta', ''),
                    'total_net': float(item.get('WartoscNetto', 0)),
                    'total_gross': float(item.get('WartoscBrutto', 0)),
                    'currency': item.get('Waluta', 'PLN'),
                    'payment_status': item.get('StatusPlatnosci', 'unpaid'),
                    'paid_amount': float(item.get('KwotaZaplacona', 0)),
                    'remaining_amount': float(item.get('Pozostalo', 0)),
                    'items': self._parse_invoice_items(item.get('Pozycje', [])),
                }
                for item in items[:limit]
            ]

        except Exception as e:
            print(f"Error fetching invoices: {e}")
            return []

    def _parse_invoice_items(self, items: List[Dict]) -> List[Dict]:
        """Helper do parsowania pozycji faktury"""
        return [
            {
                'product_code': item.get('KodTowaru', ''),
                'product_name': item.get('NazwaTowaru', ''),
                'quantity': float(item.get('Ilosc', 0)),
                'unit': item.get('Jednostka', 'szt'),
                'price_net': float(item.get('CenaNetto', 0)),
                'vat_rate': int(item.get('StawkaVAT', 23)),
                'total_net': float(item.get('WartoscNetto', 0)),
                'total_gross': float(item.get('WartoscBrutto', 0)),
            }
            for item in items
        ]

    def get_invoice_detail(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz szczegóły faktury

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"invoices/{invoice_id}"

        try:
            data = self._request('GET', endpoint)

            return {
                'invoice_id': data.get('Id', invoice_id),
                'invoice_number': data.get('Numer', ''),
                'invoice_type': data.get('TypDokumentu', 'FS'),
                'invoice_date': data.get('DataWystawienia', ''),
                'sale_date': data.get('DataSprzedazy', ''),
                'due_date': data.get('TerminPlatnosci', ''),
                'customer_code': data.get('KodKontrahenta', ''),
                'customer_name': data.get('NazwaKontrahenta', ''),
                'total_net': float(data.get('WartoscNetto', 0)),
                'total_gross': float(data.get('WartoscBrutto', 0)),
                'currency': data.get('Waluta', 'PLN'),
                'payment_status': data.get('StatusPlatnosci', 'unpaid'),
                'paid_amount': float(data.get('KwotaZaplacona', 0)),
                'remaining_amount': float(data.get('Pozostalo', 0)),
                'items': self._parse_invoice_items(data.get('Pozycje', [])),
            }

        except Exception as e:
            print(f"Error fetching invoice {invoice_id}: {e}")
            return None

    # ========== DOKUMENTY WZ ==========

    def get_customer_delivery_notes(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz dokumenty WZ

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"customers/{customer_code}/delivery-notes"

        params = {
            'customer_code': customer_code,
            'limit': limit,
        }

        if date_from:
            params['date_from'] = date_from.isoformat()

        if date_to:
            params['date_to'] = date_to.isoformat()

        try:
            data = self._request('GET', endpoint, params=params)
            items = data if isinstance(data, list) else data.get('results', [])

            return [
                {
                    'document_id': item.get('Id', ''),
                    'document_number': item.get('Numer', ''),
                    'document_type': 'WZ',
                    'document_date': item.get('Data', ''),
                    'customer_code': customer_code,
                    'customer_name': item.get('NazwaKontrahenta', ''),
                    'related_invoice': item.get('PowiazanaFaktura', ''),
                    'related_order': item.get('PowiazaneZamowienie', ''),
                    'items': self._parse_delivery_items(item.get('Pozycje', [])),
                }
                for item in items[:limit]
            ]

        except Exception as e:
            print(f"Error fetching delivery notes: {e}")
            return []

    def _parse_delivery_items(self, items: List[Dict]) -> List[Dict]:
        """Helper do parsowania pozycji WZ"""
        return [
            {
                'product_code': item.get('KodTowaru', ''),
                'product_name': item.get('NazwaTowaru', ''),
                'quantity': float(item.get('Ilosc', 0)),
                'unit': item.get('Jednostka', 'szt'),
            }
            for item in items
        ]

    # ========== PŁATNOŚCI ==========

    def get_customer_payments(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz płatności

        TODO: Wypełnij endpoint
        """
        # TODO: Wpisz endpoint
        endpoint = f"customers/{customer_code}/payments"

        params = {
            'customer_code': customer_code,
            'limit': limit,
        }

        if date_from:
            params['date_from'] = date_from.isoformat()

        if date_to:
            params['date_to'] = date_to.isoformat()

        try:
            data = self._request('GET', endpoint, params=params)
            items = data if isinstance(data, list) else data.get('results', [])

            return [
                {
                    'payment_id': item.get('Id', ''),
                    'payment_date': item.get('Data', ''),
                    'amount': float(item.get('Kwota', 0)),
                    'currency': item.get('Waluta', 'PLN'),
                    'payment_method': item.get('FormaPlatnosci', 'transfer'),
                    'related_invoice': item.get('PowiazanaFaktura', ''),
                    'description': item.get('Opis', ''),
                }
                for item in items[:limit]
            ]

        except Exception as e:
            print(f"Error fetching payments: {e}")
            return []

    # ========== STATYSTYKI ==========

    def get_customer_summary(self, customer_code: str) -> Dict[str, Any]:
        """
        Pobierz podsumowanie klienta

        TODO: Możesz zaimplementować jako pojedynczy endpoint lub agregację wielu
        """
        # Opcja 1: Endpoint zwracający gotowe statystyki
        # endpoint = f"customers/{customer_code}/summary"
        # return self._request('GET', endpoint)

        # Opcja 2: Agregacja z wielu źródeł
        try:
            orders = self.get_customer_orders(customer_code, limit=1000)
            invoices = self.get_customer_invoices(customer_code, limit=1000)

            unpaid_invoices = [inv for inv in invoices if inv['payment_status'] in ['unpaid', 'partial']]
            overdue_invoices = [
                inv for inv in unpaid_invoices
                if inv.get('due_date') and inv['due_date'] < date.today().isoformat()
            ]

            return {
                'total_orders': len(orders),
                'total_orders_value': sum(o['total_gross'] for o in orders),
                'total_invoices': len(invoices),
                'total_invoices_value': sum(i['total_gross'] for i in invoices),
                'unpaid_invoices': len(unpaid_invoices),
                'unpaid_amount': sum(i['remaining_amount'] for i in unpaid_invoices),
                'overdue_invoices': len(overdue_invoices),
                'overdue_amount': sum(i['remaining_amount'] for i in overdue_invoices),
                'last_order_date': max([o['order_date'] for o in orders], default=''),
                'last_invoice_date': max([i['invoice_date'] for i in invoices], default=''),
                'last_payment_date': '',  # TODO: dodaj jeśli masz endpoint payments
            }

        except Exception as e:
            print(f"Error calculating summary: {e}")
            return {
                'total_orders': 0,
                'total_orders_value': 0,
                'total_invoices': 0,
                'total_invoices_value': 0,
                'unpaid_invoices': 0,
                'unpaid_amount': 0,
                'overdue_invoices': 0,
                'overdue_amount': 0,
                'last_order_date': '',
                'last_invoice_date': '',
                'last_payment_date': '',
            }

    # ========== UTILITY ==========

    def get_api_info(self) -> Dict[str, str]:
        """Informacje o API"""
        return {
            'name': 'Comarch ERP XL',
            'version': '2.0',  # TODO: pobierz dynamicznie jeśli API to oferuje
            'base_url': self.base_url,
            'status': 'connected' if self.test_connection() else 'disconnected',
        }
