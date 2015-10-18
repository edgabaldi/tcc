from django.test import TestCase

class HomeTestCase(TestCase):

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
