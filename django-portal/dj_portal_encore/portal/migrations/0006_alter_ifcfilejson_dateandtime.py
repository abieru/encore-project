# Generated by Django 3.2.7 on 2021-11-21 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_alter_ifcfilejson_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ifcfilejson',
            name='dateAndTime',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]