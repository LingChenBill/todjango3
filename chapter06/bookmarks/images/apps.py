from django.apps import AppConfig


class ImagesConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        """
        导入signal处理器.
        :return:
        """
        import images.signals
