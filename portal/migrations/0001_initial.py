# Generated by Django 2.2 on 2020-12-02 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200, null=True)),
                ('dob', models.DateTimeField(null=True)),
                ('gender', models.BooleanField(default=0)),
            ],
        ),
    ]