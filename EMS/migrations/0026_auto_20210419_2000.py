# Generated by Django 3.1.7 on 2021-04-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0025_monthsalary'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthsalary',
            name='dateCreated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='monthsalary',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
