# Generated by Django 4.0.3 on 2024-01-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='image_url',
        ),
        migrations.AddField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
