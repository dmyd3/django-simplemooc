# Generated by Django 2.2 on 2019-07-12 13:57

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_thread_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=('name',), unique=True, verbose_name='Identificador'),
        ),
    ]
