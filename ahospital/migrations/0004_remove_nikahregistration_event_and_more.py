# Generated by Django 5.1.2 on 2025-01-02 13:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ahospital', '0003_delete_ok_remove_nikahregistration_applicant_bride_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nikahregistration',
            name='event',
        ),
        migrations.AddField(
            model_name='nikahregistration',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=2),
            preserve_default=False,
        ),
    ]
