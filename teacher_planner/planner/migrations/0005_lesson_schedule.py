# Generated by Django 3.1.6 on 2021-02-15 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_auto_20210213_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='planner.schedule'),
        ),
    ]
