# Generated by Django 2.2 on 2020-12-08 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_remove_detai_ten'),
    ]

    operations = [
        migrations.AddField(
            model_name='detai',
            name='TenDeTai',
            field=models.CharField(default='', max_length=1000),
        ),
    ]