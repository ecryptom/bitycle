# Generated by Django 3.1.7 on 2021-04-19 23:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0011_auto_20210327_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 19, 23, 40, 53, 896631, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 19, 23, 40, 53, 897083, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Base_currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('symbol', models.CharField(max_length=10)),
                ('persian_name', models.CharField(max_length=25)),
                ('logo', models.ImageField(null=True, upload_to='logos')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange.currency')),
            ],
        ),
    ]
