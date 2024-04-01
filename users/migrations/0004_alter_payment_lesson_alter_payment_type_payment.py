# Generated by Django 4.2.7 on 2024-03-07 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_alter_lesson_options_course_price'),
        ('users', '0003_payment_data_create_payment_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='lesson',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.DO_NOTHING, to='materials.lesson', verbose_name='оплаченный урок'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='type_payment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='способ платежа'),
        ),
    ]
