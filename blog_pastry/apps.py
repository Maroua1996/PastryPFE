from django.apps import AppConfig


class BlogPastryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_pastry'

    def ready(self) -> None:
        import blog_pastry.signals
 