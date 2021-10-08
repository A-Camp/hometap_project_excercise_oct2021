# tests/test_models.py
import factory
from ..models import Home
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = False


class HomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Home

    owner = factory.SubFactory(UserFactory)
    address = factory.Faker('street_address')
    zipcode = factory.Faker('zipcode')
    city = factory.Faker('city')
    state = factory.Faker('state_abbr')
    has_septic = factory.Faker('pybool')
    user_septic_info = factory.Faker('text')
