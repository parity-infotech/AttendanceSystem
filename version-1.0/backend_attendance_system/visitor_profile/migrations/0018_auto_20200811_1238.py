# Generated by Django 3.0 on 2020-08-11 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_profile', '0017_auto_20200811_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_time_record',
            field=models.TimeField(default=datetime.time(12, 37, 58, 595749)),
        ),
    ]