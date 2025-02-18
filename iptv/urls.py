"""
URL configuration for web_iptv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import login_iptv, dvbt_list, dvbt_edit, tools, streams_list, streams_add, content_remove, streams_remove
from .views import groups_add, groups_list, groups_remove, stb_list, stb_edit, sort_by_place, sort_by_ip, sort_by_mac
from .views import stb_remove, dvbt_change, convert, sort_by_group, vod, logout_iptv

urlpatterns = [
    path('streams/remove/<int:stream_id>/<int:content_id>', content_remove, name='content_remove'),
    path('streams/remove/<int:stream_id>', streams_remove, name='streams_remove'),
    path('streams/add', streams_add, name='streams_add'),
    path('streams/<int:stream_id>', streams_list, name='streams_list'),
    path('groups/remove/<int:groups_id>', groups_remove, name='groups_remove'),
    path('groups/<int:groups_id>', groups_list, name='groups_list'),
    path('groups/add', groups_add, name='groups_add'),
    path('stb/edit/sort_by_group', sort_by_group, name='sort_by_group'),
    path('stb/edit/sort_by_place', sort_by_place, name='sort_by_place'),
    path('stb/edit/sort_by_mac', sort_by_mac, name='sort_by_mac'),
    path('stb/edit/sort_by_ip', sort_by_ip, name='sort_by_ip'),
    path('stb/edit/<int:stb_id>', stb_edit, name='stb_edit'),
    path('stb/edit', stb_list, name='stb_list'),
    path('stb/remove/<int:stb_id>', stb_remove, name='stb_edit'),
    path('tools', tools, name='tools'),
    path('convert', convert, name='convert'),
    path('vod', vod, name='vod'),
    path('dvbt/change/<int:dvbt_id>', dvbt_change, name='dvbt_change'),
    path('dvbt/<int:dvbt_id>/<int:dvbt_list_id>', dvbt_edit, name='dvbt_edit'),
    path('dvbt/<int:dvbt_id>', dvbt_list, name='dvbt_list'),
    path('logout', logout_iptv, name='logout_iptv'),
    path('login', login_iptv, name='iptv_panel'),
    path('', login_iptv, name='iptv_panel'),
]
