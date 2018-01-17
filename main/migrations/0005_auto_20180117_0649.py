# Generated by Django 2.0.1 on 2018-01-17 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_challenge_regex_input_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backend_name', models.CharField(help_text='Verbose name for admin use.', max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(help_text='Markdown Field')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backend_name', models.CharField(help_text='Verbose name for admin use.', max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('use_custom_description', models.BooleanField(help_text='If unchecked, description from the competition schema will be used.')),
                ('custom_description', models.TextField(help_text='Markdown Field')),
                ('use_custom_welcome_message', models.BooleanField(help_text='If unchecked, welcome message from the competition schema will be used.')),
                ('custom_welcome_message', models.TextField(help_text='Markdown Field')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_open', models.BooleanField(default=True, help_text='If unchecked, users will be unable to register for this or access this unless they are already assigned to this.')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backend_name', models.CharField(help_text='Verbose name for admin use.', max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('default_description', models.TextField(help_text='Markdown Field')),
                ('default_welcome_message', models.TextField(help_text='Markdown Field')),
                ('challenge_groups', models.ManyToManyField(to='main.ChallengeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='UserParticipationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='backend_name',
            field=models.CharField(default='Favorite Fruit', help_text='Verbose name for admin use.', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challenge',
            name='challenge_unlock_dependencies',
            field=models.ManyToManyField(to='main.Challenge'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='challenge_unlock_min_points',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='data_file',
            field=models.FileField(blank=True, help_text='If the challenges needs multiple files, zip them up.', null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='userparticipationrecord',
            name='challenges_solved',
            field=models.ManyToManyField(to='main.Challenge'),
        ),
        migrations.AddField(
            model_name='userparticipationrecord',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Competition'),
        ),
        migrations.AddField(
            model_name='userparticipationrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='competition',
            name='schema',
            field=models.ManyToManyField(to='main.CompetitionSchema'),
        ),
        migrations.AddField(
            model_name='competition',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='challengegroup',
            name='challenges',
            field=models.ManyToManyField(to='main.Challenge'),
        ),
    ]
