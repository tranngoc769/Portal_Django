# Generated by Django 2.2 on 2020-12-11 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_thongbao_tieude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thongbao',
            name='IdUser',
        ),
    ]