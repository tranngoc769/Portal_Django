# Generated by Django 2.2 on 2020-12-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20201207_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='nguoidung',
            name='HoatDong',
            field=models.BooleanField(default=True),
        ),
    ]
