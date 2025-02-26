# Generated by Django 4.2.16 on 2025-01-23 07:22

from django.db import migrations, models
import django.db.models.deletion
import sending.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_running', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Статус рассылки',
                'verbose_name_plural': 'Статусы рассылок',
            },
        ),
        migrations.CreateModel(
            name='SendAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(db_index=True, verbose_name='Дата и время попытки')),
                ('status', models.BooleanField(verbose_name='Статус попытки')),
                ('response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('story_attempt', models.TextField(default='Не было рассылки пока', verbose_name='История попыток')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
            },
        ),
        migrations.CreateModel(
            name='Sending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=sending.models.Sending.default_sending_name, max_length=150, verbose_name='Название рассылки')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки')),
                ('period', models.CharField(choices=[('minute', 'Раз в минуту'), ('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=50, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена'), ('canceled', 'Отменена')], default='created', max_length=50, verbose_name='Статус рассылки')),
                ('number_of_parcels', models.IntegerField(default=1, verbose_name='Количество писем')),
                ('clients', models.ManyToManyField(to='clients.client', verbose_name='Клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'permissions': [('custom_view_sending', 'Can view sending'), ('canceled_sending', 'Can cancel sending'), ('uncanceled_sending', 'Can uncancel sending'), ('view_user_list', 'Can view user list'), ('custom_view_user', 'Can view user'), ('ban_user', 'Can ban user'), ('unban_user', 'Can unban user')],
            },
        ),
    ]
