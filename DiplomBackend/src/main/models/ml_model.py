from django.db import models

from diplom import settings


class MlModel(models.Model):
    path_to_file = models.FilePathField(path=settings.MEDIA_ROOT, blank=True)


    class Meta:
        db_table = 'ml_model'
        verbose_name = 'модель машинного обучения'
        verbose_name_plural = 'модели машинного обучения'