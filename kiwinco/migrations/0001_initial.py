# Generated by Django 4.2.1 on 2023-05-15 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemId', models.PositiveIntegerField()),
                ('itemName', models.CharField(max_length=30)),
                ('buyerId', models.PositiveIntegerField()),
                ('itemSize', models.CharField(max_length=3)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=30)),
                ('Description', models.CharField(max_length=200)),
                ('Price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('Stock_XS', models.IntegerField(default=0)),
                ('Stock_S', models.IntegerField(default=0)),
                ('Stock_M', models.IntegerField(default=0)),
                ('Stock_L', models.IntegerField(default=0)),
                ('Stock_XL', models.IntegerField(default=0)),
                ('Featured', models.BooleanField()),
                ('Jumper_Jacket', models.BooleanField()),
                ('Shirt', models.BooleanField()),
                ('Pants', models.BooleanField()),
                ('Image', models.ImageField(upload_to='images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=30)),
                ('itemSize', models.CharField(max_length=3)),
                ('buyerId', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
    ]
