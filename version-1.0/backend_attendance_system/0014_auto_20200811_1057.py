# Generated by Django 3.0 on 2020-08-11 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0013_auto_20200809_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeintime',
            name='emp_s_num',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='employee_profile.EmployeeRecord'),
        ),
    ]
