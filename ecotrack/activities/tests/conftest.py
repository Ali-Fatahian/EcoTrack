from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from ecotrack.activities.models import Activity
from ecotrack.activities.models import Category


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="test_username",
        password="test_password",
        email="test_user@gmail.com",
        name="Test User",
    )


@pytest.fixture
def other_user():
    """
    This user is built for testing permissions.
    """
    return get_user_model().objects.create_user(
        username="test_other_username",
        password="test_other_password",
        email="test_other_user@gmail.com",
        name="Test Other User",
    )


@pytest.fixture
def category():
    return Category.objects.create(name="Flug", icon="🛩️", co2_factor=Decimal(".255"))


@pytest.fixture
def activity(user, category):
    return Activity.objects.create(
        user=user,
        category=category,
        quantity=10,
        unit="km",
        date=timezone.now().date(),
        description="Test Drive",
    )
