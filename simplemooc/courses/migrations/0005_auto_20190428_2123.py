# Generated by Django 2.2 on 2019-04-28 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190421_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=models.TextField(blank=True, max_length=80, verbose_name='Descricao simples'),
        ),
    ]
