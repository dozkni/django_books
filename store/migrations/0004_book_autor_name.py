# Generated by Django 3.2.8 on 2021-10-12 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_book_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='autor_name',
            field=models.CharField(default='author', max_length=255),
            preserve_default=False,
        ),
    ]
