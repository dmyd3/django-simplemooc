# Generated by Django 2.2 on 2019-07-12 14:02

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20190712_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from='title', unique=True, verbose_name='Identificador'),
        ),
    ]