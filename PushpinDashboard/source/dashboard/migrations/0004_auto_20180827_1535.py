# Generated by Django 2.1 on 2018-08-27 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20180827_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pushpinstatconn',
            options={'ordering': ['-time_stamp', 'conn_id']},
        ),
        migrations.AlterModelOptions(
            name='pushpinstatreport',
            options={'ordering': ['-time_stamp']},
        ),
        migrations.AlterModelOptions(
            name='pushpinstatsub',
            options={'ordering': ['-time_stamp']},
        ),
    ]
