# Generated by Django 5.0.1 on 2024-02-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five', '0009_userdetails_userqualifications_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='age',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(blank=True, default='Not Specified', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='name',
            field=models.CharField(blank=True, default='Not Specified', max_length=255, null=True),
        ),
    ]
