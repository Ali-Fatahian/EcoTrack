from django.urls import path

from . import views

app_name = "activities"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("activities/", views.ActivityListView.as_view(), name="activity-list"),
]
