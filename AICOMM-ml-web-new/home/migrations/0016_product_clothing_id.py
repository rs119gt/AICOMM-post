# Generated by Django 5.0 on 2024-04-27 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='clothing_id',
            field=models.IntegerField(null=True),
        ),
    ]