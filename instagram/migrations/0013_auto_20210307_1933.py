# Generated by Django 3.1.7 on 2021-03-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0012_auto_20210306_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(max_length=1000),
        ),
    ]
