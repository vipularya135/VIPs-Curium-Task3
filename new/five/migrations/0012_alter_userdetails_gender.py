# Generated by Django 5.0.1 on 2024-02-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five', '0011_alter_userqualifications_education_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(blank=True, default='Not Specified', max_length=255, null=True),
        ),
    ]
