# Generated by Django 3.1.7 on 2021-04-02 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0016_auto_20210402_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedailywork',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employeedailywork',
            name='projectId',
            field=models.IntegerField(null=True),
        ),
    ]