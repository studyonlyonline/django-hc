# Generated by Django 2.0 on 2019-01-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0006_auto_20180922_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=255)),
                ('variant_value', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='mapped_variant',
            field=models.ManyToManyField(to='home_module.Variants'),
        ),
    ]
