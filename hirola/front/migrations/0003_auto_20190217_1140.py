# Generated by Django 2.0.2 on 2019-02-17 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_auto_20190214_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='date',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='updated',
            new_name='modified_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.Cart'),
        ),
    ]