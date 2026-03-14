"""Module for all Form Tests."""

from decimal import Decimal

import pytest
from django.utils.translation import gettext_lazy as _

from ecotrack.users.forms import UserAdminCreationForm
from ecotrack.users.forms import UserProfileForm
from ecotrack.users.models import User


class TestUserAdminCreationForm:
    """
    Test class for all tests related to the UserAdminCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Tests UserAdminCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserAdminCreationForm(
            {
                "username": user.username,
                "password1": user.password,
                "password2": user.password,
            },
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _("This username has already been taken.")


@pytest.mark.django_db
def test_user_profile_form_valid():
    """
    Test that the form accepts a valid positive decimal number.
    """
    form_data = {"monthly_goal": 160.50}
    form = UserProfileForm(data=form_data)

    assert form.is_valid() is True
    assert form.cleaned_data["monthly_goal"] == Decimal("160.50")


@pytest.mark.django_db
def test_user_profile_form_negative_invalid():
    """
    Test that the form rejects negative numbers.
    """
    form_data = {"monthly_goal": -10.00}
    form = UserProfileForm(data=form_data)

    assert form.is_valid() is False
    assert "monthly_goal" in form.errors


@pytest.mark.django_db
def test_user_profile_form_zero_valid():
    """
    Test that 0.00 is allowed (edge case).
    """
    form_data = {"monthly_goal": 0.00}
    form = UserProfileForm(data=form_data)

    assert form.is_valid() is True
    assert form.cleaned_data["monthly_goal"] == Decimal("0.00")
