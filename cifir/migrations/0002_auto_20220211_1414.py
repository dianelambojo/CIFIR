# Generated by Django 3.1.1 on 2022-02-11 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cifir', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(upload_to='media'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(upload_to='media'),
        ),
    ]
