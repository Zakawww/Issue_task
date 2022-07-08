from django.contrib import admin

from webapp.models import Issue, Status, Type


class IssueAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status', 'type', 'create_date', 'updated_date']
    list_filter = ['status', 'type']
    search_fields = ['summary']


admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Issue, IssueAdmin)
