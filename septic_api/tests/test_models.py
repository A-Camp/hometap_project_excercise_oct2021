# tests/test_models.py
from django.test import TestCase
from .factories import HomeFactory


class HomeModelTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        home = HomeFactory()
        self.assertEqual(str(home), str(home.id))