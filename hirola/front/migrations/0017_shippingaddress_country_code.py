# Generated by Django 2.0.2 on 2019-06-01 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0016_auto_20190601_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.CountryCode'),
        ),
    ]