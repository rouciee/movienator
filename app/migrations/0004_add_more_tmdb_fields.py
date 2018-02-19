# Generated by Django 2.0.1 on 2018-02-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_add_overview_and_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='budget',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_language',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='revenue',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='spoken_languages',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='status',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='tagline',
            field=models.CharField(max_length=256, null=True),
        ),
    ]