# Generated by Django 5.1.2 on 2025-01-09 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aashfApp', '0002_rename_registration_vol_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='myVol_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_Name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=255)),
                ('nid', models.ImageField(upload_to='vol_nid', verbose_name='Upload NID')),
                ('Present_Address', models.TextField()),
                ('Permanent_Address', models.TextField()),
                ('image', models.ImageField(upload_to='vol_reg', verbose_name='Upload Your Picture')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_event', to='aashfApp.event')),
            ],
        ),
        migrations.DeleteModel(
            name='Vol_Registration',
        ),
    ]
