# Generated by Django 2.0.2 on 2019-02-17 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0006_auto_20190217_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotdeal',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_model_list', to='front.PhoneModelList'),
        ),
    ]
