from django.apps import AppConfig


class ReportConfig(AppConfig):
    name = 'report'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        try:
            import zoom.signals  # noqa F401
        except ImportError:
            pass
