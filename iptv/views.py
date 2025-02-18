import os
from subprocess import Popen
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Dvbt, Dvbt_List, Streams, Streams_List, Groups, Stb_Type, Stb

stb_sort = 'ip_address'
DB_dvbt = Dvbt.objects.all()
DB_Streams = Streams.objects.prefetch_related('content').all().order_by('udp_ip')
DB_Groups = Groups.objects.all()
DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
DB_Stb_Type = Stb_Type.objects.all()

def load_all_streams():
    data = []
    db = Dvbt_List.objects.order_by('udp_ip')
    for dvbt in db:
        if dvbt.udp_ip and dvbt.udp_port:
            data.append((f'{dvbt.udp_ip}:{dvbt.udp_port}', dvbt.name))
    for db in DB_Streams:
        if db.udp_ip and db.udp_port:
            data.append((f'{db.udp_ip}:{db.udp_port}', db.name))
    return data

# Возвращает список файлов контента
def load_content_dir(directory):
    dirs = os.walk(directory)
    files = []
    for f in dirs:
        d = f[0].replace(directory, '')
        for df in f[2]:
            files.append(f'{d}\\{df}'[1:])
    return files

def rewrite_mcast(dvb_id):
    dvbt_all = Dvbt_List.objects.filter(dvbt__id=dvb_id).select_related('dvbt')
    mcast = ''
    for dvb in dvbt_all:
        if dvb.udp_ip and dvb.udp_port:
            mcast += f'{dvb.udp_ip}:{dvb.udp_port} 1 {dvb.sid}\n'
    with open(f'mcast-{str(dvb_id)}.conf', 'w') as f:
        f.write(mcast)
    print(f'systemctl restart mcast-{str(dvb_id)}.service')

def make_stream(udp_ip, udp_port):
    print(f'sh make-stream.sh {udp_ip} {udp_port}')

def remove_stream(udp_ip):
    print(f'sh rm-stream.sh {udp_ip}')

def remove_group_html(group_id):
    global DB_Stb_Type
    for stb_t in DB_Stb_Type:
        os.remove(f'{stb_t.server_path}\group-{group_id}.html')

def homepage_gen(group):
    global DB_Stb_Type
    all_stream = load_all_streams()
    stream_list = []
    stream_num = 1
    for ch, _ in all_stream:
        stream_list.append((stream_num, ch))
        if ch == group.start_stream:
            stream_start = stream_num
        stream_num += 1

    context = {
        "stream_start": stream_start,
        "stream_list": stream_list,
    }

    for stb_t in DB_Stb_Type:
        if stb_t:
            hp = render_to_string(f'{stb_t.temp_html}', context=context)
            with open(f'{stb_t.server_path}\\group-{group.id}.html', 'w') as html:
                html.write(hp)

def dhcp_gen():
    global DB_Stb
    dhcp = ''
    for stb in DB_Stb:
        if stb.group and stb.stb_type:
            context = {
                "Stb_id": stb.id,
                "Stb_mac": stb.mac_address,
                "Stb_ip": stb.ip_address,
                "Home_page": stb.stb_type.home_page,
                "Stb_group": stb.group.id,
            }
            dhcp += render_to_string(f'{stb.stb_type.temp_dhcp}', context=context)
    with open('d:\serv\dhcp\dhcp.mac', 'w') as f:
        f.write(dhcp)

# Обработка пути /
def login_iptv(request: HttpRequest):
    context = {
        'error': '',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tools')
        else:
            context['error'] = 'Ошибка ...'
    return render(request, 'iptv/login.html', context=context)

def logout_iptv(request: HttpRequest):
    logout(request)
    return redirect('iptv_panel')

# Обработка пути /tools/
@login_required(login_url='iptv/login/')
def tools(request: HttpRequest):
    global DB_dvbt, DB_Streams, DB_Groups
    with open('log.txt', 'r') as log:
        log_data = log.read()
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Log": log_data,
    }
    return render(request, 'iptv/tools.html', context=context)

@login_required(login_url='iptv/login/')
def convert(request: HttpRequest):
    if request.method == 'POST':
        print('Выполняется перекодирование ....')
        print(request.POST.get('source'))
        print(request.POST.get('file_name'))
        return redirect('tools')

    global DB_dvbt, DB_Streams, DB_Groups
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Files": load_content_dir('d:\\serv\\storage\\convert'),
    }
    return render(request, 'iptv/convert.html', context=context)

@login_required(login_url='iptv/login/')
def vod(request: HttpRequest):
    if request.method == 'POST':
        print('Выполняется VOD ....')
        content = '/storage/content/' + request.POST.get('content')
        stream = request.POST.get('stream')
        udp_ip = stream[:stream.find(':')]
        print(f'systemctl stop {udp_ip}.service')
        print(f'ffmpeg -re -i {content} -codec copy -f mpegts udp://{stream}')
        print(f'systemctl start {udp_ip}.service')
        return redirect('tools')

    global DB_dvbt, DB_Streams, DB_Groups
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Files": load_content_dir('d:\\serv\\storage\\content'),
    }
    return render(request, 'iptv/vod.html', context=context)

# Обработка пути /dvbt/id
@login_required(login_url='/login/')
def dvbt_list(request: HttpRequest, dvbt_id):
    global DB_dvbt, DB_Streams, DB_Groups
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Dvbt_current": Dvbt.objects.get(id=dvbt_id),
        "Dvbt_list" : Dvbt_List.objects.filter(dvbt__id=dvbt_id),
    }
    return render(request, 'iptv/dvbt_list.html', context=context)

@login_required(login_url='/login/')
def dvbt_change(request: HttpRequest, dvbt_id):
    global DB_dvbt, DB_Streams, DB_Groups
    dvbt = Dvbt.objects.get(id=dvbt_id)
    dvbt.active = not dvbt.active
    dvbt.save()
    DB_dvbt = Dvbt.objects.all()
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Dvbt_current": Dvbt.objects.get(id=dvbt_id),
        "Dvbt_list": Dvbt_List.objects.filter(dvbt__id=dvbt_id),
    }
    return render(request, 'iptv/dvbt_list.html', context=context)

# Обработка пути /dvbt/id/list
@login_required(login_url='/login/')
def dvbt_edit(request: HttpRequest, dvbt_id, dvbt_list_id):
    global DB_dvbt, DB_Streams, DB_Groups
    ch_edit = Dvbt_List.objects.get(id=dvbt_list_id)

    if request.method == 'POST':
        ch_edit.udp_ip = request.POST.get('udp_ip')
        ch_edit.udp_port = request.POST.get('udp_port')
        ch_edit.save()
        rewrite_mcast(dvbt_id)
        return redirect('dvbt_list', dvbt_id)

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Dvbt_current": Dvbt.objects.get(id=dvbt_id),
        "Dvbt_list" : Dvbt_List.objects.filter(dvbt__id=dvbt_id),
        "Ch_edit": ch_edit,
    }
    return render(request, 'iptv/dvbt_list_edit.html', context=context)

# Обработка пути /streams/id
@login_required(login_url='/login/')
def streams_list(request: HttpRequest, stream_id):
    if request.method == 'POST':
        stream = Streams.objects.get(id=stream_id)
        stream.content.create(source=request.POST.get('source'), name=request.POST.get('name'))
        # Создать ссылку на видео в папке канала
        print(f'ln -s /storage/content/{request.POST.get('source')} /iptv/streams/{stream.udp_ip}')
        return redirect('streams_list', stream_id)

    global DB_dvbt, DB_Streams, DB_Groups
    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Streams_id": Streams.objects.get(id=stream_id),
        "Content": Streams.objects.get(id=stream_id).content.all(),
        "Files": load_content_dir('d:\\serv\\storage\\content'),
    }
    return render(request, 'iptv/streams_list.html', context=context)

# Обработка пути /streams/add
@login_required(login_url='/login/')
def streams_add(request: HttpRequest):
    global DB_dvbt, DB_Streams, DB_Groups

    if request.method == 'POST':
        stream = Streams.objects.create(udp_ip=request.POST.get('udp_ip'))
        stream.udp_port = request.POST.get('udp_port')
        stream.name = request.POST.get('name')
        stream.save()
        DB_Streams = Streams.objects.all().order_by('udp_ip')
        make_stream(stream.udp_ip, stream.udp_port)
        return redirect('streams_list', stream.id)

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
    }
    return render(request, 'iptv/streams_add.html', context=context)

# Обработка пути /streams/remove/stream_id
@login_required(login_url='/login/')
def streams_remove(request: HttpRequest, stream_id):
    global DB_Streams
    stream = Streams.objects.get(id=stream_id)
    cont = Streams.objects.get(id=stream_id).content.all()
    for c in cont:
        c.delete()
    remove_stream(stream.udp_ip)
    stream.delete()
    DB_Streams = Streams.objects.all().order_by('udp_ip')
    return redirect('tools')

# Обработка пути /streams/remove/stream_id/content_id
@login_required(login_url='/login/')
def content_remove(request: HttpRequest, stream_id, content_id):
    cont = Streams_List.objects.get(id=content_id)
    stream = Streams.objects.get(id=stream_id)
    # Удаление ссылки на контент
    print(f'rm /iptv/streams/{stream.udp_ip}/{cont.source}')
    stream.content.remove(cont)
    return redirect('streams_list', stream_id)

# Обработка пути /groups/add
@login_required(login_url='/login/')
def groups_add(request: HttpRequest):
    global DB_dvbt, DB_Streams, DB_Groups

    if request.method == 'POST':
        group = Groups.objects.create(name=request.POST.get('group'))
        group.start_stream = request.POST.get('start_stream')
        group.save()
        homepage_gen(group)
        DB_Groups = Groups.objects.all()
        return redirect('tools')

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Stream_all": load_all_streams(),
    }
    return render(request, 'iptv/groups_add.html', context=context)

# Обработка пути /groups/groups_id
@login_required(login_url='/login/')
def groups_list(request: HttpRequest, groups_id):
    global DB_dvbt, DB_Streams, DB_Groups

    if request.method == 'POST':
        group = Groups.objects.get(id=groups_id)
        group.start_stream = request.POST.get('start_stream')
        group.save()
        homepage_gen(group)
        DB_Groups = Groups.objects.all()
        print('Переключить все приставки в группе ...')
        return redirect('tools')

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Groups_list": Groups.objects.get(id=groups_id),
        "Stream_all": load_all_streams(),
    }
    return render(request, 'iptv/groups_list.html', context=context)

@login_required(login_url='/login/')
def groups_remove(request: HttpRequest, groups_id):
    global DB_Groups, DB_Stb
    try:
        Groups.objects.get(id=groups_id).delete()
    except IntegrityError as err:
        print(f'Ошибка: {err}')
    DB_Groups = Groups.objects.all()
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    remove_group_html(int(groups_id))
    return redirect('tools')

@login_required(login_url='/login/')
def stb_remove(request: HttpRequest, stb_id):
    global DB_Stb
    Stb.objects.get(id=stb_id).delete()
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    dhcp_gen()
    return redirect('stb_list')

@login_required(login_url='/login/')
def stb_edit(request: HttpRequest, stb_id):
    global DB_dvbt, DB_Streams, DB_Groups, DB_Stb, DB_Stb_Type, stb_sort

    if request.method == 'POST':
        stb = Stb.objects.get(id=stb_id)
        stb.ip_address = request.POST.get('ip_addr')
        stb.place = request.POST.get('place')
        stb.group = Groups.objects.get(id=int(request.POST.get('group')))
        stb.save()
        DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
        dhcp_gen()
        return redirect('stb_list')

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Stb_list": DB_Stb,
        "Stb_cur": Stb.objects.get(id=stb_id),
        "Stb_type": DB_Stb_Type,
    }
    return render(request, 'iptv/stb_edit.html', context=context)

@login_required(login_url='/login/')
def stb_list(request: HttpRequest):
    global stb_sort, DB_dvbt, DB_Streams, DB_Groups, DB_Stb, DB_Stb_Type

    if request.method == 'POST':
        stb = Stb.objects.create(ip_address=request.POST.get('ip_addr'))
        stb.mac_address = request.POST.get('mac_addr')
        stb.place = request.POST.get('place')
        stb.stb_type = Stb_Type.objects.get(id=int(request.POST.get('stb_type')))
        stb.group = Groups.objects.get(id=int(request.POST.get('group')))
        stb.save()
        DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
        dhcp_gen()
        return redirect('stb_list')

    context = {
        "User": "operator",
        "Dvbt": DB_dvbt,
        "Streams": DB_Streams,
        "Groups": DB_Groups,
        "Stb_list": DB_Stb,
        "Stb_type": DB_Stb_Type,
    }
    return render(request, 'iptv/stb_list.html', context=context)

@login_required(login_url='/login/')
def sort_by_ip(request: HttpRequest):
    global stb_sort, DB_Stb
    stb_sort = 'ip_address'
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    return redirect('stb_list')

@login_required(login_url='/login/')
def sort_by_mac(request: HttpRequest):
    global stb_sort, DB_Stb
    stb_sort = 'mac_address'
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    return redirect('stb_list')

@login_required(login_url='/login/')
def sort_by_place(request: HttpRequest):
    global stb_sort, DB_Stb
    stb_sort = 'place'
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    return redirect('stb_list')

@login_required(login_url='/login/')
def sort_by_group(request: HttpRequest):
    global stb_sort, DB_Stb
    stb_sort = 'group__name'
    DB_Stb = Stb.objects.order_by(stb_sort).select_related("group", "stb_type")
    return redirect('stb_list')
