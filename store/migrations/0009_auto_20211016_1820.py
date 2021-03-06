# Generated by Django 3.2.8 on 2021-10-16 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0008_userbookrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='users_readers', through='store.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
