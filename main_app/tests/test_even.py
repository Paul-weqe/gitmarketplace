from django.test import TestCase
from main_app.services import users
from django.contrib.auth.models import User

def is_even(number):
    return number % 2 == 0

class TestIsEven(TestCase):
    def test_with_even_number(self):
        self.assertEqual(is_even(20), True)

    def test_with_odd_number(self):
        self.assertEqual(is_even(3), False)

