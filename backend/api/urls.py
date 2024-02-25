from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AmbassadorsViewSet, BudgetViewSet


router = DefaultRouter()

router.register(r'ambassadors', AmbassadorsViewSet, basename='ambassadors')
router.register(r'budget', BudgetViewSet, basename='budget')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/', include(router.urls)),
]
