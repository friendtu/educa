# Generated by Django 2.1.7 on 2021-04-09 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_text_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=True, related_name='modules', to='courses.Course'),
        ),
    ]
