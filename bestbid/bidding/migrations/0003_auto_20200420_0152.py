# Generated by Django 3.0.5 on 2020-04-19 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0002_auto_20200419_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionedasset',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bidding.Asset'),
        ),
        migrations.AlterField(
            model_name='auctionedasset',
            name='auction_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bidding.Auction'),
        ),
        migrations.AlterField(
            model_name='auctionedasset',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bidding.Buyer'),
        ),
        migrations.AlterField(
            model_name='auctionedasset',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bidding.Seller'),
        ),
    ]
