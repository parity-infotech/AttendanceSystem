# Generated by Django 3.0.8 on 2020-08-03 22:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0005_auto_20200803_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendanceverification',
            name='emp_s_num',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee_profile.EmployeeRecord'),
        ),
        migrations.AlterField(
            model_name='employeeintime',
            name='emp_entry_time',
            field=models.TimeField(default=datetime.time(22, 24, 57, 142599)),
        ),
    ]
