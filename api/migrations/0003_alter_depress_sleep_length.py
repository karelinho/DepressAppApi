# Generated by Django 3.2.6 on 2021-09-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210914_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depress',
            name='sleep_length',
            field=models.TextField(blank=True, default='0', max_length=256),
        ),
    ]
