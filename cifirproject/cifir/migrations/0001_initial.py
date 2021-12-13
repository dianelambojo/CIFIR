# Generated by Django 3.1.1 on 2021-12-13 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('author', models.CharField(max_length=250)),
                ('cover', models.ImageField(upload_to='media/')),
                ('file', models.FileField(upload_to='media/')),
                ('isFavorite', models.BooleanField(default=False)),
                ('isHaveRead', models.BooleanField(default=False)),
                ('isToRead', models.BooleanField(default=False)),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Books',
                'db_table': 'Book',
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('link', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('cover', models.CharField(max_length=250)),
                ('defaultUsername', models.CharField(max_length=150)),
                ('defaultPassword', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Catalogs',
                'db_table': 'Catalog',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.CharField(max_length=250)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes_book', to='cifir.book')),
            ],
            options={
                'verbose_name_plural': 'Notes',
                'db_table': 'Note',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('isDeleted', models.BooleanField(default=False)),
                ('book', models.ManyToManyField(blank=True, to='cifir.Book')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Collections',
                'db_table': 'Collection',
            },
        ),
    ]
