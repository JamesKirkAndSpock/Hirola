# Generated by Django 2.0.2 on 2019-06-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0015_auto_20190601_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]