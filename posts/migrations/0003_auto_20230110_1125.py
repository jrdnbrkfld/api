# Generated by Django 3.2.16 on 2023-01-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_image_filter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_filter',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('html', 'HTML'), ('css', 'CSS'), ('javascript', 'JavaScript'), ('react', 'React')], max_length=50, null=True),
        ),
    ]
