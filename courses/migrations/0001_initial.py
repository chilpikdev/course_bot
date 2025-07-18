# Generated by Django 5.2.4 on 2025-07-06 16:18

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название курса')),
                ('description', models.TextField(help_text='Подробное описание курса для пользователей', verbose_name='Описание курса')),
                ('short_description', models.CharField(blank=True, help_text='Краткое описание для отображения в списке', max_length=300, verbose_name='Краткое описание')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена курса в рублях', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Цена')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, help_text='Старая цена для показа скидки', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Старая цена')),
                ('group_link', models.URLField(help_text='Пригласительная ссылка в Telegram группу/канал', verbose_name='Ссылка на группу')),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to='courses/images/', verbose_name='Изображение курса')),
                ('is_active', models.BooleanField(default=True, help_text='Доступен ли курс для покупки', verbose_name='Активен')),
                ('is_featured', models.BooleanField(default=False, help_text='Показывать ли курс в рекомендуемых', verbose_name='Рекомендуемый')),
                ('max_students', models.PositiveIntegerField(blank=True, help_text='Максимальное количество студентов (оставьте пустым для неограниченного)', null=True, verbose_name='Максимум студентов')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название способа оплаты')),
                ('card_number', models.CharField(blank=True, max_length=20, verbose_name='Номер карты')),
                ('cardholder_name', models.CharField(blank=True, help_text='ФИО владельца карты', max_length=200, verbose_name='Получатель')),
                ('bank_name', models.CharField(blank=True, max_length=100, verbose_name='Название банка')),
                ('instructions', models.TextField(blank=True, verbose_name='Инструкции по оплате')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Способ оплаты',
                'verbose_name_plural': 'Способы оплаты',
                'ordering': ['order', 'name'],
            },
        ),
    ]
