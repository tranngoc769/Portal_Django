# Generated by Django 2.2 on 2020-12-06 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_nguoidung_mssv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nguoidung',
            old_name='MSSV',
            new_name='TenNguoiDung',
        ),
    ]
