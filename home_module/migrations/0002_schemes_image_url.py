# Generated by Django 2.0 on 2018-09-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemes',
            name='image_url',
            field=models.URLField(default=None),
        ),
    ]
