# Generated by Django 2.1 on 2021-04-18 13:38

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20210417_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=embed_video.fields.EmbedVideoField(),
        ),
    ]