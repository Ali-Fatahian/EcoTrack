from django.urls import path

from . import views

app_name = "activities"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("activities/", views.ActivityListView.as_view(), name="list"),
    path("activities/add", views.ActivityCreateView.as_view(), name="create"),
    path("activities/<int:pk>/edit", views.ActivityUpdateView.as_view(), name="update"),
    path(
        "activities/<int:pk>/delete", views.ConfirmDeleteView.as_view(), name="delete"
    ),
]
