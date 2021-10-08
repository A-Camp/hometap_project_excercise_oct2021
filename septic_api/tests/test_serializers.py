# tests/test_serializers.py
from django.test import TestCase

from ..serializers import HomeSerializer
from .factories import HomeFactory, UserFactory


class HomeSerializerTestCase(TestCase):
    def setUp(self):
        # Set up serializer and instance of modal from same data.
        self.home = HomeFactory()
        self.serializer = HomeSerializer(self.home)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'address', 'zipcode', 'city', 'state', 'owner', 'has_septic', 'user_septic_info']
        )

    def test_field_content(self):
        self.assertEqual(
            self.serializer.data['id'],
            str(getattr(self.home, 'id'))
        )
        self.assertEqual(
            self.serializer.data['owner'],
            str(getattr(self.home, 'owner'))
        )
        for field_name in [
            'address', 'zipcode', 'city', 'state', 'has_septic', 'user_septic_info'
        ]:
            self.assertEqual(
                self.serializer.data[field_name],
                getattr(self.home, field_name)
            )

        