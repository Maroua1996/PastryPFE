# Generated by Django 4.2.4 on 2023-08-19 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_pastry', '0002_alter_article_slug_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='aticle',
            new_name='article',
        ),
    ]
