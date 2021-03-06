# Generated by Django 2.1 on 2021-03-25 07:09

import courses.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('courses', '0002_auto_20210324_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('order', courses.fields.OrderField(blank=True)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ['text', 'file', 'image', 'video']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='module',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='module',
            name='object_id',
        ),
        migrations.AddField(
            model_name='module',
            name='order',
            field=courses.fields.OrderField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='courses.Module'),
        ),
    ]
