from django.contrib import admin

from ambassadors.models import StudyProgramm, Ambassadors


@admin.register(StudyProgramm)
class StudyProgrammAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    ordering = ('id',)


@admin.register(Ambassadors)
class AmbassadorsAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'date_created')
    search_fields = ('surname', 'name', 'patronymic', 'date_created')
    ordering = ('surname', 'name', 'patronymic', 'date_created')
