# Generated by Django 4.2.7 on 2024-03-11 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_alter_lesson_options_course_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stripe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_product', models.CharField(max_length=100, verbose_name='ID продукта из stripe')),
                ('stripe_price', models.CharField(max_length=100, verbose_name='ID стоимости из stripe')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.course', verbose_name='Курс')),
            ],
        ),
    ]
