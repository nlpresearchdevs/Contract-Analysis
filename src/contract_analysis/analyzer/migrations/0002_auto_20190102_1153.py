# Generated by Django 2.1.4 on 2019-01-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='keywords',
            field=models.FileField(blank=True, null=True, upload_to='media/keywords/'),
        ),
    ]
