# Generated by Django 2.0.2 on 2019-03-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20190305_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_change_allowed',
            field=models.BooleanField(default=False, help_text='Designates whether this user has been authorized to change his own password, in the change_password view.', verbose_name='change_allowed'),
        ),
    ]
