# Generated by Django 4.2.5 on 2024-03-20 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vardhaman', '0033_order_cgst_amount_order_sgst_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firebase_token',
            new_name='expo_go_token',
        ),
    ]
