from django.contrib import admin
from .models import Dvbt, Dvbt_List, Streams, Streams_List, Groups, Stb_Type, Stb

@admin.register(Dvbt)
class DvbtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'freq', 'active')

@admin.register(Dvbt_List)
class Dvbt_ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sid', 'udp_ip', 'udp_port', 'dvbt__name')

@admin.register(Streams)
class StreamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'udp_ip', 'udp_port', 'name', 'group__name')

@admin.register(Streams_List)
class StreamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'name')

@admin.register(Groups)
class StreamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_stream')

@admin.register(Stb_Type)
class StreamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'name', 'remote_control', 'login', 'password', 'temp_html', 'temp_dhcp', 'home_page', 'server_path')

@admin.register(Stb)
class StreamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'mac_address', 'place', 'group__name', 'stb_type__model')
