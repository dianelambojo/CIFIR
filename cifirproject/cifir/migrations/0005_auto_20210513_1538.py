# Generated by Django 3.1.1 on 2021-05-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cifir', '0004_collection_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='cover',
            field=models.CharField(max_length=250),
        ),
    ]
