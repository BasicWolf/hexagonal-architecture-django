# Generated by Django 3.2 on 2021-05-02 12:15
from uuid import UUID

from django.db import migrations


def populate_demo_user_and_article_data(apps, schema_editor):
    VotingUserEntity = apps.get_model('myapp', 'VotingUserEntity')
    VotingUserEntity.objects.create(
        user_id=UUID('e47cec00-c22a-486d-afe6-e76902f211c1'),
        karma=10
    )


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_demo_user_and_article_data)
    ]
