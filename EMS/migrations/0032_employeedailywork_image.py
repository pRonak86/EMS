# Generated by Django 3.1.7 on 2021-05-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0031_employeedailywork_employeename'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedailywork',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
