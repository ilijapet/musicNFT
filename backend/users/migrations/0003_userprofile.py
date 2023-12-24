# Generated by Django 4.2.7 on 2023-12-23 12:05

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0001_initial"),
        ("users", "0002_alter_newuser_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("eth_address", models.CharField(blank=True, max_length=100)),
                ("payment_type", models.CharField(default="Undefined", max_length=20)),
                ("total_no_of_nfts", models.IntegerField(default=0)),
                ("total_paid", models.FloatField(default=0)),
                (
                    "nft_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(blank=True, null=True),
                        default=list,
                        size=None,
                    ),
                ),
                ("nft_metadata", models.ManyToManyField(to="dashboard.nftmetadata")),
                (
                    "user",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]