# Generated by Django 4.1.1 on 2022-11-24 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('protocol_type', models.IntegerField(choices=[(1, 'Bitcoin'), (90001, 'Bitcoin (Testnet)')])),
                ('block_id', models.IntegerField(db_index=True)),
                ('block_hash', models.CharField(max_length=255)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_orphan', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddConstraint(
            model_name='block',
            constraint=models.UniqueConstraint(fields=('protocol_type', 'block_id', 'block_hash'), name='block_unique'),
        ),
    ]