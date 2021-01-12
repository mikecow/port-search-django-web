from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('self_del/<int:pid>', views.index_del, name='self_del'),
    path('local_ip', views.local_ip, name='local_ip'),
    path('local_ip_port/<str:ip>', views.local_ip_port, name='local_ip_port'),
    path('search_any_port', views.search_any_port, name='search_any_port'),
    path('search', views.search, name='search'),
    path('listen', views.listen, name='listen'),
    path('listen_port/<str:ip>', views.listen_port, name='listen_port'),
    path('kill_port/<str:ip>/<int:pid>', views.kill_port, name='kill_port'),
    path('quit_con/<str:ip>', views.quit_con, name='quit_con')
]
