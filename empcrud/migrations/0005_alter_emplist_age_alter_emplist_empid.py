# Generated by Django 4.0.5 on 2022-07-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empcrud', '0004_alter_emplist_age_alter_emplist_empid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emplist',
            name='age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='emplist',
            name='empid',
            field=models.PositiveIntegerField(),
        ),
    ]