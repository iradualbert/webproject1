# Generated by Django 3.0.2 on 2020-03-29 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0002_auto_20200328_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availability_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_pictures', to='Business.Product'),
        ),
        migrations.AlterField(
            model_name='productanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='Business.ProductQuestion'),
        ),
        migrations.AlterField(
            model_name='productquestion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_questions', to='Business.Product'),
        ),
        migrations.AlterField(
            model_name='userguide',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_information', to='Business.Product'),
        ),
        migrations.AlterField(
            model_name='userguidelanguageversion',
            name='user_guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_version', to='Business.UserGuide'),
        ),
    ]
