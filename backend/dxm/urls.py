from django.urls import path

from .views import getRelogio, setRelogio
from .views import Reboot, Travar, Destravar, getRegs, setRegs

urlpatterns = [  
    path('getrelogio/',getRelogio, name="get-Relogio"),
    path('setrelogio/',setRelogio, name="set-Relogio"),
    path('reboot/',Reboot, name="reboot"),
    path('travar/',Travar, name="travar"),
    path('destravar/',Destravar, name="destravar"),
    path('getregs/',getRegs, name="get-regs"),
    path('setregs/',setRegs, name="set-regs")
]