from django.contrib import admin

from ecotrack.activities.models import Activity
from ecotrack.activities.models import Category

admin.site.register(Category)
admin.site.register(Activity)
