# Generated by Django 4.2.6 on 2024-05-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usermedicalinfo_lifestyleinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpersonalinfo',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
