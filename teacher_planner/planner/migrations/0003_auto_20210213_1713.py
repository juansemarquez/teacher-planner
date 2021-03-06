# Generated by Django 3.1.6 on 2021-02-13 17:13

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('planner', '0002_auto_20210210_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='similar_lessons',
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyphrase', models.CharField(max_length=100)),
                ('lessons', models.ManyToManyField(related_name='tags', to='planner.Lesson')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='planner.teacher')),
            ],
        ),
        migrations.AlterField(
            model_name='classgroup',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classgroups', to='planner.teacher'),
        ),
        migrations.AlterField(
            model_name='file',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='planner.teacher'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='planner.teacher'),
        ),
        migrations.AlterField(
            model_name='material',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='planner.teacher'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='planner.teacher'),
        ),
        migrations.AlterField(
            model_name='school',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='planner.teacher'),
        ),
    ]
