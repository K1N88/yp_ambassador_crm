from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AmbassadorsViewSet, StudyProgrammViewSet,
                       SupervisorViewSet, ContentViewSet)


router = DefaultRouter()

router.register('ambassadors', AmbassadorsViewSet)
router.register('supervisors', StudyProgrammViewSet)
router.register('study_programms', SupervisorViewSet)
router.register('content', ContentViewSet, basename='content')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/', include(router.urls)),
]
