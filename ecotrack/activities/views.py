import csv
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from ecotrack.activities.forms import ActivityForm
from ecotrack.activities.models import Activity


class IsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "activities/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        user = self.request.user

        activities_this_month = Activity.objects.filter(
            user=user, date__year=now.year, date__month=now.month
        )
        monthly_sum = (
            activities_this_month.aggregate(monthly_sum=Sum("co2_amount"))[
                "monthly_sum"
            ]
            or 0
        )  # Just in case it returns None

        category_co2_breakdown = (
            Activity.objects.filter(
                user=user, date__year=now.year, date__month=now.month
            )
            .values("category__name")
            .annotate(cat_sum=Sum("co2_amount"))
            .order_by("-cat_sum")
        )

        labels = [item["category__name"].title() for item in category_co2_breakdown]
        data = [float(item["cat_sum"]) for item in category_co2_breakdown]

        monthly_goal = user.profile.monthly_goal
        if monthly_goal > 0:
            progress_percentage = (monthly_sum / monthly_goal) * 100
        else:
            progress_percentage = 0

        last_five_activities = Activity.objects.filter(user=user)[:5]

        context["monthly_sum"] = monthly_sum
        context["monthly_goal"] = monthly_goal
        context["breakdown"] = category_co2_breakdown
        context["chart_labels"] = json.dumps(labels)
        context["chart_data"] = json.dumps(data)
        context["progress_percentage"] = progress_percentage
        context["recent_activities"] = last_five_activities

        return context


class ActivityListView(ListView):
    model = Activity
    template_name = "activity_list.html"
    context_object_name = "activities"
    paginate_by = 10

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class ActivityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/activity_form.html"
    success_message = "The new activity was successfully created!"

    def get_success_url(self):
        return reverse("activities:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ActivityUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, IsOwnerMixin, UpdateView
):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/activity_form.html"
    success_message = "The activity was updated!"

    def get_success_url(self):
        return reverse("activities:list")


class ConfirmDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, IsOwnerMixin, DeleteView
):
    model = Activity
    template_name = "activities/activity_confirm_delete.html"
    success_message = "The activity was deleted!"

    def get_success_url(self):
        return reverse("activities:list")


@login_required
def export_activities_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="my_activities.csv"'},
    )

    writer = csv.writer(response)

    writer.writerow([f"EcoTrack Activity Log - Generated on {timezone.now().date()}"])

    writer.writerow(["Date", "Category", "Quantity", "Unit", "CO2 (kg)", "Description"])

    activities = request.user.activities.all().select_related("category")

    for activity in activities:
        writer.writerow(
            [
                activity.date,
                activity.category.name,
                activity.quantity,
                activity.unit,
                activity.co2_amount,
                activity.description,
            ]
        )

    return response
