# Generated by Django 3.0.8 on 2020-08-17 23:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_profile', '0022_auto_20200817_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_time_record',
            field=models.TimeField(default=datetime.time(23, 46, 10, 12201)),
        ),
    ]
