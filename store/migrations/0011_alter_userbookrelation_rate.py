# Generated by Django 3.2.8 on 2021-10-16 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20211016_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Bad'), (2, 'Ok'), (3, 'Fine'), (4, 'Good'), (5, 'Best')], null=True),
        ),
    ]
