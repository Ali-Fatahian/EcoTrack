from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from ecotrack.activities.models import Activity
from ecotrack.activities.models import Category


@pytest.mark.django_db
def test_category_creation():
    """
    Verify that a new category is created with the expected fields' values after
    providing all the required data.
    """
    category = Category.objects.create(
        name="Auto", icon="🚗", co2_factor=Decimal(".21")
    )

    assert category.pk
    assert category.name == "Auto"
    assert category.icon == "🚗"
    assert category.slug == "auto"
    assert category.co2_factor == Decimal(".21")


@pytest.mark.django_db
def test_category_slug_unique():
    """
    Verify that two categories with the same exact name therefore the same slug
    fields can not exist in the database
    """

    Category.objects.create(name="Auto", icon="🚗", co2_factor=Decimal(".21"))

    with pytest.raises(IntegrityError):
        Category.objects.create(name="Auto", icon="🚗", co2_factor=Decimal(".21"))


@pytest.mark.django_db
def test_category_field_requirements():
    """
    Check that the correct Category model's fields are required and optional.
    """

    category_no_slug = Category.objects.create(
        name="Auto", icon="🚗", co2_factor=Decimal(".21")
    )
    category_no_name = Category.objects.create(icon="🚗", co2_factor=Decimal(".21"))
    category_no_icon = Category.objects.create(name="Auto 2", co2_factor=Decimal(".21"))

    with pytest.raises(ValidationError):
        category_no_name.full_clean()
    with pytest.raises(ValidationError):
        category_no_icon.full_clean()
    with pytest.raises(IntegrityError):
        Category.objects.create(name="Auto 3", icon="🚗")  # No co2_factor

    assert category_no_slug.pk


@pytest.mark.django_db
def test_activity_creation(user, category):
    """
    Verify that a new activity is created with the expected fields' values after
    providing all the required data.
    """
    activity = Activity.objects.create(
        user=user, category=category, quantity=Decimal("1200.5"), unit="km"
    )

    assert activity.pk


@pytest.mark.django_db
def test_activity_required_fields(user, category):
    """
    Verify that the correct fields are required for creating a new activity.
    """
    activity_missing_user = Activity(
        category=category, quantity=Decimal("10.0"), unit="km"
    )
    with pytest.raises(ValidationError):
        activity_missing_user.full_clean()

    activity_missing_category = Activity(user=user, quantity=Decimal("10.0"), unit="km")
    with pytest.raises(ValidationError):
        activity_missing_category.full_clean()

    activity_missing_quantity = Activity(user=user, category=category, unit="km")
    with pytest.raises(ValidationError):
        activity_missing_quantity.full_clean()


@pytest.mark.django_db
def test_activity_co2_amount_calculation(user, category):
    """
    Check that the algorithm for calculating the CO2 amount
    (quantity * co2_factor) is working properly.
    """
    activity = Activity.objects.create(
        user=user, category=category, quantity=Decimal("1200.5"), unit="km"
    )
    # Force reload from DB to get the rounded value
    activity.refresh_from_db()

    assert activity.co2_amount == Decimal(
        "306.128"
    )  # 0.255 is the CO2 factor used by the category fixture (Flug)


@pytest.mark.django_db
def test_activity_negative_quantity_value(user, category):
    """
    Check that a user can not provide a negative value for the quantity.
    """

    activity = Activity.objects.create(
        user=user, category=category, quantity=Decimal("-50"), unit="km"
    )

    with pytest.raises(ValidationError):
        activity.full_clean()  # Validation check does not apply to .create


@pytest.mark.django_db
def test_activity_defaults_to_today(user, category):
    """
    Verify that when users don't provide the date,
    the default value of it is today.
    """

    activity = Activity.objects.create(
        user=user, category=category, quantity=Decimal("200.00"), unit="km"
    )

    assert activity.date is not None
    assert activity.date.date() == timezone.now().date()
