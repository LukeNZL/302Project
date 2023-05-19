# Generated by Django 4.1.1 on 2023-05-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwinco', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carteditem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='price',
        ),
        migrations.AlterField(
            model_name='item',
            name='Price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='carteditem',
            name='Price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='Price',
            field=models.IntegerField(default=0),
        ),
    ]
