# Generated by Django 3.1.4 on 2020-12-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20201207_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0),
        ),
    ]
