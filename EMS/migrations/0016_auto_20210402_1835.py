# Generated by Django 3.1.7 on 2021-04-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0015_employeedailywork'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedailywork',
            name='clientId',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='employeedailywork',
            name='logoutTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employeedailywork',
            name='workDescription',
            field=models.CharField(max_length=40, null=True),
        ),
    ]