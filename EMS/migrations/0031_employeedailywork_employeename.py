# Generated by Django 3.1.7 on 2021-05-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0030_attendance_employeename'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedailywork',
            name='employeeName',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
