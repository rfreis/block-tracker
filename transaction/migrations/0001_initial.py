# Generated by Django 4.1.1 on 2022-12-05 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_usd', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_asset', models.CharField(max_length=255)),
                ('asset_name', models.CharField(max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s', to='wallet.address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutputData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_usd', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_asset', models.CharField(max_length=255)),
                ('asset_name', models.CharField(max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s', to='wallet.address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('protocol_type', models.IntegerField(choices=[(1, 'Bitcoin'), (90001, 'Bitcoin (Testnet)')])),
                ('tx_id', models.CharField(db_index=True, max_length=255)),
                ('block_id', models.IntegerField(blank=True, null=True)),
                ('block_time', models.DateTimeField(blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_orphan', models.BooleanField(default=False)),
                ('details', models.JSONField(default=dict)),
                ('inputs', models.ManyToManyField(db_index=True, related_name='inputs', through='transaction.InputData', to='wallet.address')),
                ('outputs', models.ManyToManyField(db_index=True, related_name='outputs', through='transaction.OutputData', to='wallet.address')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='outputdata',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s', to='transaction.transaction'),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s', to='transaction.transaction'),
        ),
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.UniqueConstraint(fields=('protocol_type', 'tx_id'), name='transaction_unique'),
        ),
    ]
