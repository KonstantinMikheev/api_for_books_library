# Generated by Django 5.1.4 on 2024-12-15 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_genre_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(help_text='авторы', to='library.author'),
        ),
    ]