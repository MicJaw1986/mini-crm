"""
Abstrakcyjny interfejs dla klientów ERP

INSTRUKCJA:
1. BaseERPClient definiuje "kontrakt" - co każdy ERP musi umieć
2. Implementuj konkretne metody w klasie dziedziczącej (np. ComarchERPClient)
3. Każda metoda zwraca standardowy format dict/list - niezależnie od API ERP
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime, date


class BaseERPClient(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich klientów ERP

    Każdy konkretny klient ERP (Comarch, SAP, własny) musi zaimplementować te metody.
    """

    # ========== KONTRAHENCI (CUSTOMERS) ==========

    @abstractmethod
    def get_customer(self, customer_code: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz dane pojedynczego kontrahenta

        Args:
            customer_code: Kod kontrahenta w ERP

        Returns:
            {
                'code': 'KH001',
                'name': 'Firma ABC Sp. z o.o.',
                'nip': '1234567890',
                'address': 'ul. Przykładowa 1, 00-001 Warszawa',
                'email': 'kontakt@firmaabc.pl',
                'phone': '+48 123 456 789',
                'payment_terms': '14 dni',  # termin płatności
                'credit_limit': 50000.00,   # limit kredytu
                'balance': 12500.50,        # saldo (dodatnie = nasz dług, ujemne = ich dług)
            }
        """
        pass

    @abstractmethod
    def search_customers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Wyszukaj kontrahentów po nazwie/NIP/kodzie

        Args:
            query: Fraza do wyszukiwania
            limit: Max liczba wyników

        Returns:
            Lista słowników jak w get_customer()
        """
        pass

    # ========== ZAMÓWIENIA (ORDERS) ==========

    @abstractmethod
    def get_customer_orders(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz zamówienia klienta

        Args:
            customer_code: Kod kontrahenta
            date_from: Data od (opcjonalnie)
            date_to: Data do (opcjonalnie)
            limit: Max liczba wyników

        Returns:
            [
                {
                    'order_id': 'ZAM/2024/001',
                    'order_number': 'ZAM/2024/001',
                    'order_date': '2024-01-15',
                    'customer_code': 'KH001',
                    'customer_name': 'Firma ABC',
                    'total_net': 10000.00,
                    'total_gross': 12300.00,
                    'currency': 'PLN',
                    'status': 'confirmed',  # draft/confirmed/in_progress/completed/cancelled
                    'delivery_date': '2024-01-20',
                    'items': [
                        {
                            'product_code': 'PROD001',
                            'product_name': 'Produkt XYZ',
                            'quantity': 10,
                            'unit': 'szt',
                            'price_net': 100.00,
                            'total_net': 1000.00,
                        }
                    ]
                }
            ]
        """
        pass

    @abstractmethod
    def get_order_detail(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz szczegóły pojedynczego zamówienia

        Args:
            order_id: ID/numer zamówienia

        Returns:
            Słownik jak w get_customer_orders() z pełnymi szczegółami
        """
        pass

    # ========== FAKTURY SPRZEDAŻOWE (INVOICES) ==========

    @abstractmethod
    def get_customer_invoices(
        self,
        customer_code: str,
        invoice_type: Optional[str] = None,  # 'FS', 'FKOR', 'FP', etc.
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz faktury klienta

        Args:
            customer_code: Kod kontrahenta
            invoice_type: Typ faktury (FS, FKOR, FP, etc.) - None = wszystkie
            date_from: Data od
            date_to: Data do
            limit: Max liczba wyników

        Returns:
            [
                {
                    'invoice_id': 'FS/2024/001',
                    'invoice_number': 'FS/2024/001',
                    'invoice_type': 'FS',  # FS, FKOR, FP
                    'invoice_date': '2024-01-15',
                    'sale_date': '2024-01-15',
                    'due_date': '2024-01-29',  # termin płatności
                    'customer_code': 'KH001',
                    'customer_name': 'Firma ABC',
                    'total_net': 10000.00,
                    'total_gross': 12300.00,
                    'currency': 'PLN',
                    'payment_status': 'unpaid',  # paid/unpaid/overdue/partial
                    'paid_amount': 0.00,
                    'remaining_amount': 12300.00,
                    'items': [
                        {
                            'product_code': 'PROD001',
                            'product_name': 'Produkt XYZ',
                            'quantity': 10,
                            'unit': 'szt',
                            'price_net': 100.00,
                            'vat_rate': 23,
                            'total_net': 1000.00,
                            'total_gross': 1230.00,
                        }
                    ]
                }
            ]
        """
        pass

    @abstractmethod
    def get_invoice_detail(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Pobierz szczegóły pojedynczej faktury

        Args:
            invoice_id: ID/numer faktury

        Returns:
            Słownik jak w get_customer_invoices() z pełnymi szczegółami
        """
        pass

    # ========== DOKUMENTY MAGAZYNOWE (WAREHOUSE DOCUMENTS) ==========

    @abstractmethod
    def get_customer_delivery_notes(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz dokumenty WZ (wydania zewnętrzne)

        Args:
            customer_code: Kod kontrahenta
            date_from: Data od
            date_to: Data do
            limit: Max liczba wyników

        Returns:
            [
                {
                    'document_id': 'WZ/2024/001',
                    'document_number': 'WZ/2024/001',
                    'document_type': 'WZ',
                    'document_date': '2024-01-15',
                    'customer_code': 'KH001',
                    'customer_name': 'Firma ABC',
                    'related_invoice': 'FS/2024/001',  # powiązana faktura
                    'related_order': 'ZAM/2024/001',   # powiązane zamówienie
                    'items': [
                        {
                            'product_code': 'PROD001',
                            'product_name': 'Produkt XYZ',
                            'quantity': 10,
                            'unit': 'szt',
                        }
                    ]
                }
            ]
        """
        pass

    # ========== PŁATNOŚCI (PAYMENTS) ==========

    @abstractmethod
    def get_customer_payments(
        self,
        customer_code: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Pobierz historię płatności klienta

        Args:
            customer_code: Kod kontrahenta
            date_from: Data od
            date_to: Data do
            limit: Max liczba wyników

        Returns:
            [
                {
                    'payment_id': 'KP/2024/001',
                    'payment_date': '2024-01-20',
                    'amount': 12300.00,
                    'currency': 'PLN',
                    'payment_method': 'transfer',  # transfer/cash/card
                    'related_invoice': 'FS/2024/001',
                    'description': 'Płatność za FV FS/2024/001',
                }
            ]
        """
        pass

    # ========== STATYSTYKI (STATISTICS) ==========

    @abstractmethod
    def get_customer_summary(self, customer_code: str) -> Dict[str, Any]:
        """
        Pobierz podsumowanie dla klienta (do dashboardu)

        Args:
            customer_code: Kod kontrahenta

        Returns:
            {
                'total_orders': 15,
                'total_orders_value': 150000.00,
                'total_invoices': 12,
                'total_invoices_value': 148000.00,
                'unpaid_invoices': 3,
                'unpaid_amount': 25000.00,
                'overdue_invoices': 1,
                'overdue_amount': 5000.00,
                'last_order_date': '2024-01-15',
                'last_invoice_date': '2024-01-16',
                'last_payment_date': '2024-01-10',
            }
        """
        pass

    # ========== UTILITY METHODS ==========

    def test_connection(self) -> bool:
        """
        Testuj połączenie z ERP

        Returns:
            True jeśli połączenie działa
        """
        try:
            # Przykładowy test - można override w konkretnej implementacji
            result = self.search_customers(query="TEST", limit=1)
            return True
        except Exception:
            return False

    def get_api_info(self) -> Dict[str, str]:
        """
        Pobierz informacje o API (dla debug/admin)

        Returns:
            {
                'name': 'Comarch ERP XL',
                'version': '2024.0',
                'base_url': 'https://api.example.com',
                'status': 'connected',
            }
        """
        return {
            'name': self.__class__.__name__,
            'version': 'unknown',
            'base_url': 'not configured',
            'status': 'unknown',
        }
