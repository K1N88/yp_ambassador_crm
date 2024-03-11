from django.contrib import admin

from .models import Budget, MerchForSend, Merch

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('ambassador', 'merch')


class MerchAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')


class MerchForsendAdmin(admin.ModelAdmin):
    list_display = ('ambassador', 'merch', 'count', 'date',
                    'comment', 'shipped')


admin.site.register(Merch, MerchAdmin)
admin.site.register(MerchForSend, MerchForsendAdmin)
