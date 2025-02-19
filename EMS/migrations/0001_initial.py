# Generated by Django 3.1.7 on 2021-03-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('contact', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=20)),
                ('bloodGroup', models.CharField(max_length=20)),
                ('managerName', models.CharField(max_length=30, null=True)),
                ('joinDate', models.DateField(null=True)),
                ('salary', models.IntegerField(null=True)),
                ('leave', models.IntegerField(null=True)),
                ('qualification', models.CharField(max_length=30)),
                ('activation_Date', models.DateTimeField(null=True)),
                ('deactivation_Date', models.DateTimeField(null=True)),
                ('account', models.CharField(default='Deactive', max_length=20)),
                ('emailId', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('empCode', models.CharField(default='None', editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
