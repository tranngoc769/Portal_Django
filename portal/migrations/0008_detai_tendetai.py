# Generated by Django 2.2 on 2020-12-08 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20201207_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='detai',
            name='TenDeTai',
            field=models.CharField(default='Tên', max_length=1000),
            preserve_default=False,
        ),
    ]