# Generated by Django 4.2.7 on 2024-02-15 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pay', models.DateField(verbose_name='дата оплаты')),
                ('payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма платежа')),
                ('type_payment', models.CharField(max_length=100, verbose_name='способ платежа')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='materials.course', verbose_name='оплаченный курс')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='materials.lesson', verbose_name='оплаченный урок')),
                ('user_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='email студента')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]
