# Generated by Django 2.1.4 on 2019-01-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0008_remove_contract_reswatsonemotions'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='resWatsonContractElements',
            field=models.FileField(blank=True, null=True, upload_to='analyzer/results/contractElements'),
        ),
    ]