# Generated by Django 4.0.3 on 2022-07-23 23:47

import app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_project_fileext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file',
            field=models.FileField(upload_to=app.models.project_file_upload, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip', '7zip'])]),
        ),
    ]
