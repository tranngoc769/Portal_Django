# Generated by Django 2.2 on 2020-12-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_nguoidung_khoa'),
    ]

    operations = [
        migrations.CreateModel(
            name='DIEUKIENDANGKY',
            fields=[
                ('Id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('IdLoai', models.IntegerField()),
                ('IdKhoa', models.IntegerField()),
                ('Diem', models.FloatField(default=0)),
            ],
        ),
    ]
