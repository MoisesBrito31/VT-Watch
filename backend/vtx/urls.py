from django.urls import path
from .views import OsList, OsDetail
from .views import GatewayList, GatewayDetail, DxmStatus
from .views import NodeList, NodeDetail
from .views import NodeSetupList, NodeSetupDetail
from .views import HistList, HistDetail, Filtra
from .views import EventoList, EventoDetail, Eventos
from .views import Aprende, ConfigDXM

urlpatterns = [
    path('os/', OsList.as_view()),
    path('os/<int:pk>/',OsDetail.as_view()),
    path('gateway/', GatewayList.as_view()),
    path('gateway/<int:pk>/',GatewayDetail.as_view()),
    path('dxm/',DxmStatus,name="dxm-status"),
    path('node/', NodeList.as_view()),
    path('node/<int:pk>/',NodeDetail.as_view()),
    path('nodesetup/', NodeSetupList.as_view()),
    path('nodesetup/<int:pk>/',NodeSetupDetail.as_view()),
    path('hist/', HistList.as_view()),
    path('hist/<int:pk>/',HistDetail.as_view()),
    path('evento/', EventoList.as_view()),
    path('evento/<int:pk>/',EventoDetail.as_view()),    
    path('filtra/',Filtra,name="filtra"),
    path('aprende/',Aprende,name="aprende"),
    path('config/',ConfigDXM,name="config_DXM"),
    path('eventos/',Eventos.as_view(),name="eventos"),
]