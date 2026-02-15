from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ecotrack.users"
    verbose_name = _("Users")

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
        # F401: We import it for side effects (registering signals).
        # PLC0415: Django requires this inside ready(), not at the top level.
        import ecotrack.users.signals  # noqa: F401, PLC0415
