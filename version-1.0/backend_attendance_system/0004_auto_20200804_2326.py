# Generated by Django 3.0 on 2020-08-04 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_profile', '0003_auto_20200802_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetails',
            name='company_founding_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
