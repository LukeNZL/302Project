# Generated by Django 4.1.1 on 2023-05-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwinco', '0003_rename_price_carteditem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='PriceFloat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]