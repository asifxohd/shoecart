# Generated by Django 4.2.6 on 2023-11-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orders_price_remove_orders_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='status',
        ),
        migrations.AddField(
            model_name='ordersitem',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Order confirmed', max_length=20),
        ),
    ]
