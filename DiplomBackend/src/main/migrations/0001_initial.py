# Generated by Django 4.2.1 on 2023-05-16 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path_to_file', models.FilePathField(blank=True, path='media')),
            ],
        ),
    ]