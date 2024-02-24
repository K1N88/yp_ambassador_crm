from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AmbassadorsViewSet, ContentViewSet

router = DefaultRouter()

router.register('ambassadors', AmbassadorsViewSet, basename='ambassadors')
router.register('content', ContentViewSet, basename='content')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/', include(router.urls)),
]
