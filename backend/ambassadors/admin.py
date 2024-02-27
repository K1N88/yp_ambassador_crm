from django.contrib import admin

from ambassadors.models import StudyProgramm, Ambassadors, Content, ContentType


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


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('link',)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'ambassador', 'contents')
    list_filter = ('title', 'status', 'ambassador')
    search_fields = ('title', 'status', 'ambassador__name')

    def contents(self, obj):
        return [o for o in obj.contents.all()]
