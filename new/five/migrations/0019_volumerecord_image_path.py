# Generated by Django 5.0.1 on 2024-02-19 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five', '0018_alter_membership_membership_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='volumerecord',
            name='image_path',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
