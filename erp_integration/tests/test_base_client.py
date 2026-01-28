"""
Testy dla base ERP client
"""

from django.test import TestCase
from erp_integration.services.base_client import BaseERPClient


class ConcreteERPClient(BaseERPClient):
    """
    Konkretna implementacja dla testów
    """

    def get_customer(self, customer_code):
        return {
            'code': customer_code,
            'name': 'Test Company',
            'nip': '1234567890',
        }

    def search_customers(self, query, limit=10):
        return [{'code': 'TEST001', 'name': query}]

    def get_customer_orders(self, customer_code, date_from=None, date_to=None, limit=20):
        return [{'order_id': '1', 'order_number': 'ORD001', 'total_gross': 1000.00}]

    def get_order_detail(self, order_id):
        return {'order_id': order_id, 'order_number': 'ORD001'}

    def get_customer_invoices(self, customer_code, invoice_type=None, date_from=None, date_to=None, limit=20):
        return [{'invoice_id': '1', 'invoice_number': 'INV001', 'total_gross': 1230.00}]

    def get_invoice_detail(self, invoice_id):
        return {'invoice_id': invoice_id, 'invoice_number': 'INV001'}

    def get_customer_delivery_notes(self, customer_code, date_from=None, date_to=None, limit=20):
        return [{'document_id': '1', 'document_number': 'WZ001'}]

    def get_customer_payments(self, customer_code, date_from=None, date_to=None, limit=20):
        return [{'payment_id': '1', 'amount': 1230.00}]

    def get_customer_summary(self, customer_code):
        return {
            'total_orders': 5,
            'total_orders_value': 5000.00,
            'unpaid_invoices': 2,
            'unpaid_amount': 2460.00,
        }


class BaseERPClientTest(TestCase):
    """Testy dla abstrakcyjnego interfejsu"""

    def setUp(self):
        self.client = ConcreteERPClient()

    def test_get_customer(self):
        """Test pobierania klienta"""
        customer = self.client.get_customer('TEST001')
        self.assertIsNotNone(customer)
        self.assertEqual(customer['code'], 'TEST001')
        self.assertEqual(customer['name'], 'Test Company')

    def test_search_customers(self):
        """Test wyszukiwania"""
        results = self.client.search_customers('ABC')
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_get_customer_orders(self):
        """Test pobierania zamówień"""
        orders = self.client.get_customer_orders('TEST001')
        self.assertIsInstance(orders, list)
        self.assertGreater(len(orders), 0)

    def test_get_customer_invoices(self):
        """Test pobierania faktur"""
        invoices = self.client.get_customer_invoices('TEST001')
        self.assertIsInstance(invoices, list)
        self.assertGreater(len(invoices), 0)

    def test_get_customer_summary(self):
        """Test podsumowania"""
        summary = self.client.get_customer_summary('TEST001')
        self.assertIsNotNone(summary)
        self.assertIn('total_orders', summary)
        self.assertIn('unpaid_amount', summary)

    def test_get_api_info(self):
        """Test informacji o API"""
        info = self.client.get_api_info()
        self.assertIsInstance(info, dict)
        self.assertIn('name', info)
