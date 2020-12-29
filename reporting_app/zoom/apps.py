from django.apps import AppConfig


class ZoomConfig(AppConfig):
    name = 'zoom'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        try:
            import zoom.signals  # noqa F401
        except ImportError:
            pass
