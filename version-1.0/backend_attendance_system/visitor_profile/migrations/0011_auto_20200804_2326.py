# Generated by Django 3.0 on 2020-08-04 23:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_profile', '0010_auto_20200804_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_time_record',
            field=models.TimeField(default=datetime.time(23, 26, 7, 988427)),
        ),
    ]