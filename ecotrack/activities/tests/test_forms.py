from datetime import timedelta

import pytest
from django.utils import timezone

from ecotrack.activities.forms import ActivityForm
from ecotrack.activities.models import Activity


@pytest.mark.django_db
def test_activity_form_valid(category):
    """
    Test that the form is valid when all fields are correct
    and the date is today or in the past.
    """
    form_data = {
        "category": category.id,
        "quantity": 10.5,
        "unit": Activity.UnitChoices.KILOMETER,
        "date": timezone.now().date(),
        "description": "Commute to work",
    }

    form = ActivityForm(data=form_data)

    assert form.is_valid() is True
    activity = form.save(commit=False)
    assert activity.quantity == 10.5  # Check if it saves correctly


@pytest.mark.django_db
def test_activity_form_future_date_invalid(category):
    """
    Test that the form raises a ValidationError if the date is in the future.
    """
    future_date = timezone.now().date() + timedelta(days=1)

    form_data = {
        "category": category.id,
        "quantity": 5,
        "unit": Activity.UnitChoices.KILOGRAM,
        "date": future_date,
    }

    form = ActivityForm(data=form_data)

    assert form.is_valid() is False
    assert "date" in form.errors
    assert "The activity date can not be in the future." in form.errors["date"]


@pytest.mark.django_db
def test_activity_form_missing_data():
    """Test that required fields are actually required."""
    form_data = {
        "description": "Just a description, no data",
    }

    form = ActivityForm(data=form_data)

    assert form.is_valid() is False
    assert "quantity" in form.errors
    assert "category" in form.errors
    assert "date" in form.errors
