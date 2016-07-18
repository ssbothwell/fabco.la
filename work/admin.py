from django.contrib import admin

from .models import Client, Project, LineItem, ClientAddress

class LineItemInline(admin.TabularInline):
    model = LineItem

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        LineItemInline,
    ]

admin.site.register(Client)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ClientAddress)
admin.site.register(LineItem)