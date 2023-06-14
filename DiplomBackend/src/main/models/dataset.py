from django.db import models

from diplom import settings


class Dataset(models.Model):
    path_to_file = models.FilePathField(path=settings.MEDIA_ROOT, blank=True)


    class Meta:
        db_table = 'dataset'
        verbose_name = 'датасет'
        verbose_name_plural = 'датасеты'
