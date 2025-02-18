from django.db import models

# Список каналов (мультиплексов)
class Dvbt(models.Model):
    class Meta:
        ordering = ['name', ]
    name = models.CharField(max_length=20, verbose_name='Канал')
    freq = models.CharField(max_length=3, verbose_name='Частота')
    active = models.BooleanField(default=False, verbose_name='Вкл_Выкл')

# Список программ в мультиплексе
class Dvbt_List(models.Model):
    class Meta:
        ordering = ['name',]
    name = models.CharField(max_length=20, db_index=True, verbose_name='Программа')
    sid = models.CharField(max_length=5, verbose_name='SIG')
    udp_ip = models.CharField(max_length=15, blank=True, verbose_name='IP адрес')
    udp_port = models.CharField(max_length=5, blank=True, verbose_name='IP порт')
    dvbt = models.ForeignKey(Dvbt, blank=True, on_delete=models.PROTECT, related_name='dvbt_ch', verbose_name='Канал')

class Groups(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=20, unique=True, verbose_name="Имя группы")
    start_stream = models.CharField(max_length=20, blank=True, verbose_name="Старт канал")

# Список контента в потоке
class Streams_List(models.Model):
    class Meta:
        ordering = ['source',]
    source = models.CharField(max_length=254, verbose_name="Контент")
    name = models.CharField(max_length=40, blank=True, verbose_name="Примечание")

# Список потоков
class Streams(models.Model):
    class Meta:
        ordering = ['udp_ip']
    udp_ip = models.CharField(max_length=15, db_index=True, verbose_name="IP адрес")
    udp_port = models.CharField(max_length=5, verbose_name="IP порт")
    name = models.CharField(max_length=30, verbose_name="Примечание")
    content = models.ManyToManyField(Streams_List)
    group = models.ForeignKey(Groups, null=True, blank=True, on_delete=models.SET_NULL, related_name='stream', verbose_name='Группа')

# Список типов приставок
class Stb_Type(models.Model):
    class Meta:
        ordering = ['model', 'name']

    model = models.CharField(max_length=20, verbose_name="Модель")
    name = models.CharField(max_length=30, verbose_name="Примечание")
    remote_control = models.CharField(max_length=15, verbose_name="Удаленный доступ")
    login = models.CharField(max_length=20, verbose_name="Логин")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    temp_html = models.CharField(max_length=20, blank=True, verbose_name="Шаблон HTML")
    temp_dhcp = models.CharField(max_length=20, blank=True, verbose_name="Шаблон DHCP")
    home_page = models.CharField(max_length=30, blank=True, verbose_name="Домашняя страница")
    server_path = models.CharField(max_length=30, blank=True, verbose_name="Путь на сервере")

class Stb(models.Model):
    class Meta:
        ordering = ['ip_address', 'mac_address']

    mac_address = models.CharField(max_length=17, db_index=True, verbose_name="MAC адрес")
    ip_address = models.CharField(max_length=15, db_index=True, verbose_name="IP адрес")
    place = models.CharField(max_length=30, db_index=True, verbose_name="Место установки")
    group = models.ForeignKey(Groups, null=True, blank=True, on_delete=models.SET_NULL, related_name='stb_list', verbose_name='Группа')
    stb_type = models.ForeignKey(Stb_Type, null=True, blank=True, on_delete=models.SET_NULL, related_name='stb_type', verbose_name='Тип')
