from django.contrib import admin
from .models import Gateway, Node, NodeSetup, Hist, Evento, Aprendizado, AprendizadoLog

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('name','address','online')

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name','online')

@admin.register(NodeSetup)
class NodeSetupAdmin(admin.ModelAdmin):
    list_display = ('node','address','nodeId',)

@admin.register(Hist)
class HistAdmin(admin.ModelAdmin):
    list_display = ('node','time')

@admin.register(Aprendizado)
class AprendizadoAdmin(admin.ModelAdmin):
    list_display = ('id','criado','node')

@admin.register(AprendizadoLog)
class AprendizadoLogAdmin(admin.ModelAdmin):
    list_display = ('time','aprendizado')