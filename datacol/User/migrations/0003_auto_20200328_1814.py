# Generated by Django 3.0.2 on 2020-03-28 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20200323_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('new_subscriber', 'new_subscriber'), ('new_question', 'new_question'), ('new_answer', 'new_answer')], max_length=20),
        ),
    ]