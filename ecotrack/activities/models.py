from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=False, unique=True, db_index=True)
    icon = models.CharField(max_length=255)
    co2_factor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Activity(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="activities"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="activities"
    )
    description = models.TextField(blank=True, default="", max_length=500)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )  # Prevent negative values
    unit = models.CharField(max_length=20)
    date = models.DateField(
        default=timezone.now, help_text="The date the activity occurred"
    )
    co2_amount = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True, editable=False
    )  # Not intended for manual editing

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Activities model"

    def __str__(self):
        return f"Activity of type {self.category.name} by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.category.pk and self.quantity is not None:
            self.co2_amount = self.quantity * self.category.co2_factor
        super().save(*args, **kwargs)
