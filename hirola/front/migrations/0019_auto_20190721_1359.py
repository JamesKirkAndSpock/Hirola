# Generated by Django 2.0.2 on 2019-07-21 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0018_auto_20190705_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
