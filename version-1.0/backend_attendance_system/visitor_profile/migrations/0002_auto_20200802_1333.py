# Generated by Django 3.0.8 on 2020-08-02 13:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorintime',
            name='visitor_image_time_record',
            field=models.TimeField(verbose_name=datetime.time(13, 33, 30, 796883)),
        ),
    ]
