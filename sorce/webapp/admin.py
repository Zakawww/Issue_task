from django.contrib import admin

from webapp.models import Issue, Status, Type, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status', 'create_date', 'updated_date']
    list_filter = ['status']
    search_fields = ['summary']


admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)
admin.site.register(Issue, IssueAdmin)
