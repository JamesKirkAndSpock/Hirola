# Generated by Django 2.0.2 on 2019-04-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_auto_20190405_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='size',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
