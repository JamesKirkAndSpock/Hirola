# Generated by Django 2.0.2 on 2019-03-09 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_remove_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonelist',
            name='category',
        ),
        migrations.RemoveField(
            model_name='phonelist',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='phonelist',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='phonelist',
            name='size_sku',
        ),
        migrations.AlterUniqueTogether(
            name='phonescolor',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='phonescolor',
            name='color',
        ),
        migrations.RemoveField(
            model_name='phonescolor',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='phonescolor',
            name='size',
        ),
        migrations.DeleteModel(
            name='PhoneList',
        ),
        migrations.DeleteModel(
            name='PhonesColor',
        ),
    ]