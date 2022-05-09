# Generated by Django 3.1.7 on 2021-04-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0023_employeedailywork_logouthour'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('employeeId', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('loginTime', models.DateTimeField()),
                ('logoutTime', models.DateTimeField()),
                ('status', models.CharField(default='Absent', max_length=20)),
            ],
        ),
    ]