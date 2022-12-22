from django.contrib import admin
from .models import Work, Contact, Banner


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "title")
    search_fields = ("title", "description", "created_at")
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Contact)
admin.site.register(Banner)


