from django.contrib import admin
#from attachments.admin import AttachmentInlines


from .models import Client, Project, LineItem, ClientAddress

class LineItemInline(admin.TabularInline):
    model = LineItem

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        LineItemInline,
        #AttachmentInlines,
    ]

admin.site.register(Client)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ClientAddress)
admin.site.register(LineItem)