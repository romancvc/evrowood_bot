# Generated by Django 4.0.6 on 2022-08-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fewapp', '0009_rename_point_adress_pointsales_point_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointsales',
            name='contacts_point',
        ),
        migrations.AddField(
            model_name='pointsales',
            name='contacts_point_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Имя контакного лица'),
        ),
        migrations.AddField(
            model_name='pointsales',
            name='contacts_point_phone',
            field=models.CharField(max_length=12, null=True, verbose_name='Телефон контакного лица'),
        ),
    ]
