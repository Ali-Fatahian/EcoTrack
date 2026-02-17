import json
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from ecotrack.activities.models import Activity

pytestmark = pytest.mark.django_db


class TestDashboardView:
    def test_dashboard_access_redirects_anonymous(self, client):
        """
        Test the dashboard redirects anynomous requests to the Login page.
        """
        url = reverse("activities:dashboard")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response.url

    def test_dashboard_context_data(self, client, user, category):
        """
        Verify the dashboard calculates sums and breakdown correctly.
        """
        client.force_login(user)

        # 1. Create activity for this month
        Activity.objects.create(
            user=user,
            category=category,
            quantity=100,
            unit="km",
            date=timezone.now().date(),
        )  # 100 * 0.255 = 25.500 kg CO2

        # 2. Create activity for LAST month (should be ignored)
        last_month = timezone.now().date() - timedelta(days=40)
        Activity.objects.create(
            user=user, category=category, quantity=50, unit="km", date=last_month
        )

        response = client.get(reverse("activities:dashboard"))

        assert response.status_code == 200

        assert response.context["monthly_sum"] == 25.500

        # Check Goal (Default is 150.0)
        assert response.context["monthly_goal"] > 0

        labels = json.loads(response.context["chart_labels"])
        assert "Flug" in labels

        assert len(response.context["recent_activities"]) == 2


class TestActivityListView:
    def test_list_view_shows_own_activities_only(
        self, client, user, other_user, category
    ):
        """
        Verify users only see their own activities.
        """
        client.force_login(user)

        my_activity = Activity.objects.create(
            user=user, category=category, quantity=10, unit="km"
        )
        other_user_activity = Activity.objects.create(
            user=other_user, category=category, quantity=20, unit="km"
        )

        response = client.get(reverse("activities:list"))

        assert response.status_code == 200
        activities = response.context["activities"]
        assert my_activity in activities
        assert other_user_activity not in activities


class TestActivityCreateView:
    def test_create_activity(self, client, user, category):
        client.force_login(user)
        url = reverse("activities:create")

        data = {
            "category": category.id,
            "quantity": 50,
            "unit": "km",
            "date": timezone.now().date(),
            "description": "New Trip",
        }

        response = client.post(url, data)

        # Should redirect to list after success
        assert response.status_code == 302
        assert response.url == reverse("activities:list")

        assert Activity.objects.count() == 1
        activity = Activity.objects.first()
        assert activity.user == user
        assert activity.quantity == 50
