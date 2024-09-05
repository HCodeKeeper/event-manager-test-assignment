import faker
import pytest

from events.models import Event


@pytest.fixture
def test_password():
    return "password"


@pytest.fixture
def test_email():
    return "test@gmail.com"


@pytest.fixture
def user(django_user_model, test_password, test_email):
    return django_user_model.objects.create_user(
        email=test_email, password=test_password, first_name="John", last_name="Doe"
    )


@pytest.fixture
def random_user(django_user_model, test_password):
    return django_user_model.objects.create_user(
        email=faker.email(), password=test_password, first_name=faker.first_name(), last_name=faker.last_name()
    )


@pytest.fixture
def generate_events(user, random_user):
    events = []
    for _ in range(10):
        event = Event.objects.create(
            title=faker.sentence(),
            description=faker.text(),
            start=faker.date_time_this_month(),
            end=faker.date_time_this_month(),
            location=faker.address(),
            user=user,
        )
        event.participants.add(random_user)
        events.append(event)
    return events
