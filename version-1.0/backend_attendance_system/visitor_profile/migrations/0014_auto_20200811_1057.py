# Generated by Django 3.0 on 2020-08-11 10:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_profile', '0013_auto_20200809_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_date_record',
            field=models.DateField(default=datetime.date(2020, 8, 11)),
        ),
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_time_record',
            field=models.TimeField(default=datetime.time(10, 56, 49, 290429)),
        ),
    ]
