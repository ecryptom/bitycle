# Generated by Django 3.1.7 on 2021-03-23 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20210324_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='five_min_candle',
            name='number_of_trades',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='one_day_candle',
            name='number_of_trades',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='one_min_candle',
            name='number_of_trades',
            field=models.IntegerField(),
        ),
    ]
