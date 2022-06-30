# Generated by Django 4.0.4 on 2022-06-30 08:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tweets', '0002_delete_tweetmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=140)),
                ('good', models.IntegerField(blank=True, default=0, null=True)),
                ('bad', models.IntegerField(blank=True, default=0, null=True)),
                ('author', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('good_user_list', models.TextField(blank=True, default='', null=True)),
                ('bad_user_list', models.TextField(blank=True, default='', null=True)),
            ],
        ),
    ]
