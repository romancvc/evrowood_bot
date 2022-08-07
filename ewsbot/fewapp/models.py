from django.db import models

# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField('ID пользователя в Telegram', unique=True, primary_key=True)
    nickname = models.TextField('Имя пользователя')

    def __str__(self):
        return f'#{self.external_id} {self.nickname}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class User(models.Model):
    profile = models.OneToOneField(
        verbose_name='Профиль',
        to='Profile',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    full_name = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Телефон', max_length=12)
    key_auto = models.CharField('Ключ авторизации', max_length=19)
    user_id = models.CharField('ID пользователя в Telegram', max_length=20, default=0, primary_key=True)

    def __str__(self):
        return f'#{self.profile} {self.full_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Questions(models.Model):
    quest_id = models.PositiveIntegerField('ID задания', unique=True, primary_key=True)
    name_quest = models.CharField('Название задания', max_length=100)
    text_quest = models.TextField('Текст задания')

    def __str__(self):
        return f'#{self.quest_id} {self.name_quest}'

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

class UserQuestions(models.Model):
    user_id = models.ForeignKey(
        verbose_name='Профиль',
        to='User',
        on_delete=models.CASCADE
    )
    quest_id = models.ForeignKey(
        verbose_name='Задание',
        to='Questions',
        on_delete=models.CASCADE
    )
    date_ad = models.DateTimeField('Время принятия', auto_now_add=True)
    date_comletion = models.DateTimeField('Время завершения', null=True)
    completed = models.BooleanField('Выполнено', default=False)

    class Meta:
        verbose_name = 'Задание пользователя'
        verbose_name_plural = 'Задания пользователей'

class PointSales(models.Model):
    point_id = models.AutoField('ID торговой точки', unique=True, primary_key=True)
    point_name = models.CharField('Название торговой точки', max_length=100)
    metro = models.CharField('Станция метро', max_length=100, null=True)
    point_address = models.CharField('Адрес ТТ', max_length=100, null=True)
    point_number = models.CharField('Номер ТТ на рынке', max_length=20, null=True)
    point_photo = models.CharField('Фото стенда', max_length=100, null=True)
    active_led = models.CharField('Горит ли LED', max_length=5, null=True)
    stand_column = models.CharField('Стенд-колонна', max_length=5, null=True)
    handout = models.CharField('Раздаточный материал', max_length=5, null=True)
    mark_point = models.IntegerField('Оценка ТТ', null=True)
    competitor = models.TextField('Конкуренты на ТТ', null=True)
    contacts_point_name = models.CharField('Имя контакного лица', null=True, max_length=100)
    contacts_point_phone = models.CharField('Телефон контакного лица', null=True, max_length=12)
    contacts_point_email = models.CharField('Email контакного лица', null=True, max_length=30)

    def __str__(self):
        return f'#{self.point_name}'

    class Meta:
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'