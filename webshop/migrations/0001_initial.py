# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-09 23:06
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=64)),
                ('post_code', models.IntegerField()),
                ('phone_number', models.CharField(max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('brand', models.CharField(blank=True, max_length=128)),
                ('color', models.CharField(blank=True, max_length=32)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Category')),
            ],
        ),
    ]
