from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

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
