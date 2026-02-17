from django.contrib import admin

from ecotrack.activities.models import Activity
from ecotrack.activities.models import Category

admin.site.register(Category)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("date", "user", "category", "quantity", "unit", "co2_amount")

    list_filter = ("category", "date", "unit")

    search_fields = ("description", "user__username", "category__name")
