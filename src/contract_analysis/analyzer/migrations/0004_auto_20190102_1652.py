# Generated by Django 2.1.4 on 2019-01-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0003_auto_20190102_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='document',
            field=models.FileField(upload_to='contracts', verbose_name=''),
        ),
    ]
