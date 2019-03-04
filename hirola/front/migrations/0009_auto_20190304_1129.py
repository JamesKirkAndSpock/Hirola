# Generated by Django 2.0.2 on 2019-03-04 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0008_auto_20190217_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phoneimage',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='review',
            name='phone',
        ),
        migrations.AddField(
            model_name='phoneimage',
            name='images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_images', to='front.PhoneModelList'),
        ),
        migrations.AddField(
            model_name='phonemodel',
            name='brand_model_image',
            field=models.ImageField(default='brand_model_image_alt', upload_to='brand_models'),
        ),
        migrations.AddField(
            model_name='review',
            name='phone_model',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='phone_reviews', to='front.PhoneModel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=models.CharField(error_messages={'unique': 'The color you entered already exists'}, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='feature',
            name='feature',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='feature',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_features', to='front.PhoneModelList'),
        ),
        migrations.AlterField(
            model_name='phonemodellist',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_color', to='front.Color'),
        ),
        migrations.AlterField(
            model_name='phonemodellist',
            name='phone_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_list', to='front.PhoneModel'),
        ),
        migrations.AlterField(
            model_name='phonemodellist',
            name='size_sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_size', to='front.PhoneMemorySize'),
        ),
        migrations.AlterField(
            model_name='productinformation',
            name='feature',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='productinformation',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_information', to='front.PhoneModelList'),
        ),
    ]
