# Generated by Django 3.0.8 on 2020-08-03 22:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0003_auto_20200803_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeintime',
            name='emp_entry_time',
            field=models.TimeField(default=datetime.time(22, 18, 37, 464939)),
        ),
    ]