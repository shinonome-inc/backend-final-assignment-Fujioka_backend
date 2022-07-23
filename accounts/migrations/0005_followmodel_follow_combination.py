# Generated by Django 4.0.4 on 2022-07-23 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_followmodel_delete_friendship'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='followmodel',
            constraint=models.UniqueConstraint(fields=('following_user', 'follower_user'), name='follow_combination'),
        ),
    ]
