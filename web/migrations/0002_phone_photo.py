# Generated by Django 4.1.7 on 2023-07-12 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='phones/'),
        ),
    ]
