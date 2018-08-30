"""progetto_isw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^search_user_card/', views.search_user_card, name='search_user_card'),
    url(r'^search_user_board/', views.search_user_board, name='search_user_board'),
    url(r'^modify_or_delete_card/add_or_remove_user_to_card/(?P<user_id>[0-9]+)/(?P<card_id>[0-9]+)/', views.add_or_remove_user_to_card, name='add_or_remove_user_to_card'),
    url(r'^modify_or_delete_card/(?P<card_id>[0-9]+)/(?P<board_id>[0-9]+)/', views.modify_or_delete_card, name='modify_or_delete_card'),
    url(r'^add_card/(?P<board_id>\d+)/(?P<column_id>[0-9]+)/', views.add_card, name='add_card'),
    url(r'^modify_or_delete_column/(?P<column_id>[0-9]+)/(?P<board_id>[0-9]+)/', views.modify_or_delete_column, name='modify_or_delete_column'),
    url(r'^add_column/(?P<board_id>\d+)/', views.add_column, name='add_column'),
    url(r'^add_or_remove_user_to_board/(?P<board_id>[0-9]+)/(?P<user_id>[0-9]+)/', views.add_or_remove_user_to_board, name='add_or_remove_user_to_board'),
    url(r'^add_or_remove_user_to_board/(?P<board_id>[0-9]+)/', views.add_or_remove_user_to_board, name='add_or_remove_user_to_board'),
    url(r'^modify_or_delete_board/(?P<board_id>[0-9]+)/', views.modify_or_delete_board, name='modify_or_delete_board'),
    url(r'^add_board/', views.add_board, name='add_board'),
    url(r'^burndown/(?P<board_id>\d+)/', views.burndown, name='burndown'),
    url(r'^board/(?P<board_id>\d+)/', views.board_view, name='board'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^logout/', views.log_out, name='logout'),
    url(r'^about/', views.about, name='about'),
    url(r'^', views.login_signup, name='login_signup'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
