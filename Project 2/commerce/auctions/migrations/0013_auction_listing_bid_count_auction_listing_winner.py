# Generated by Django 4.1.4 on 2022-12-17 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0012_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction_listing",
            name="bid_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="auction_listing",
            name="winner",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]