from django.contrib import admin

from users.models import CrmUser


@admin.register(CrmUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    ordering = ('username',)
