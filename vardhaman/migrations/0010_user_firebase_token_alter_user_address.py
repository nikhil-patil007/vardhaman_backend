# Generated by Django 4.2.5 on 2024-01-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vardhaman', '0009_alter_user_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firebase_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
