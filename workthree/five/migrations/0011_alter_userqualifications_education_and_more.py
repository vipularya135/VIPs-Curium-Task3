# Generated by Django 5.0.1 on 2024-02-01 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five', '0010_alter_userdetails_age_alter_userdetails_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userqualifications',
            name='education',
            field=models.CharField(blank=True, default='Not Specified', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userqualifications',
            name='hobbies',
            field=models.TextField(blank=True, default='Not Specified', null=True),
        ),
    ]
