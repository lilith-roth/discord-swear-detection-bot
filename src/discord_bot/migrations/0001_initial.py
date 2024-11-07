# Generated by Django 5.1.2 on 2024-11-07 06:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DiscordServer",
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
                ("discord_server_name", models.CharField(blank=True, max_length=128)),
                ("discord_server_id", models.BigIntegerField(unique=True)),
                ("discord_swear_info_chat_id", models.BigIntegerField(default=0)),
                ("react_swears", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="DiscordServerAdminGroup",
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
                ("group_id", models.BigIntegerField()),
                (
                    "discord_server",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_bot.discordserver",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DiscordServerSwearGroup",
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
                ("group_id", models.BigIntegerField()),
                (
                    "discord_server",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_bot.discordserver",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Swear",
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
                ("swear", models.CharField(max_length=64)),
                ("added_by", models.BigIntegerField()),
                ("reaction_emoji", models.CharField(default="😡", max_length=64)),
                (
                    "added_timestamp",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "discord_server",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_bot.discordserver",
                    ),
                ),
            ],
            options={
                "unique_together": {("swear", "discord_server")},
            },
        ),
        migrations.CreateModel(
            name="SwearCount",
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
                ("swear_count", models.IntegerField(default=0)),
                ("discord_user_id", models.BigIntegerField()),
                ("discord_user_name", models.CharField(max_length=128)),
                (
                    "swear",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_bot.swear",
                    ),
                ),
            ],
            options={
                "unique_together": {("swear", "discord_user_id")},
            },
        ),
    ]
