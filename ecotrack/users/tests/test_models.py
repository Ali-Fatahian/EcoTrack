from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from ecotrack.users.models import User
from ecotrack.users.models import UserProfile


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


@pytest.mark.django_db
def test_profile_created_automatically_with_user():
    """
    Test that creating a User automatically creates a UserProfile
    via the post_save signal.
    """

    user = User.objects.create_user(username="signal_test", password="password123")

    # Check relationship (reverse accessor 'profile')
    assert hasattr(user, "profile")
    assert isinstance(user.profile, UserProfile)


@pytest.mark.django_db
def test_profile_default_monthly_goal():
    """
    Test that the profile is initialized with the correct default value for
    monthly goal of 150.00.
    """
    user = User.objects.create_user(username="defaults_test", password="pw")

    # Check the Decimal value (ensure precision matches)
    assert user.profile.monthly_goal == Decimal("150.00")


@pytest.mark.django_db
def test_profile_validation_negative_monthly_goal():
    """
    Test that the monthly_goal cannot be negative.
    """
    user = User.objects.create_user(username="negative_test", password="pw")

    # Update the auto-created profile with invalid data
    profile = user.profile
    profile.monthly_goal = Decimal("-50.00")

    with pytest.raises(ValidationError):
        profile.full_clean()
