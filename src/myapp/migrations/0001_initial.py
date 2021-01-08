import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ArticleVoteEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('article_id', models.UUIDField()),
                ('vote', models.IntegerField(choices=[(1, 'UP'), (2, 'DOWN')])),
            ],
            options={
                'db_table': 'article_vote',
                'unique_together': {('user_id', 'article_id')},
            },
        ),

        migrations.CreateModel(
            name='VoteCastingUserEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('karma', models.IntegerField()),
            ],
            options={
                'db_table': 'user_data',
            },
        ),
    ]
