# Generated by Django 4.2.5 on 2025-03-18 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vardhaman', '0002_order_order_taxes_order_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
