# Generated by Django 4.0.4 on 2022-06-08 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_catagories_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]