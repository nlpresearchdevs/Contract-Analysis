# Generated by Django 2.1.4 on 2018-12-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0006_auto_20181228_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents'),
        ),
    ]
