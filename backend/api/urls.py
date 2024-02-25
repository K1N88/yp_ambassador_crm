from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AmbassadorsViewSet, BudgetViewSet, StudyProgrammViewSet,
                       SupervisorViewSet,)
from merch.views import MerchandiseView

router = DefaultRouter()

router.register(r'ambassadors', AmbassadorsViewSet, basename='ambassadors')
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'supervisors', StudyProgrammViewSet)
router.register(r'study_programms', SupervisorViewSet)
router.register(r'merchandise', MerchandiseView, basename='merchandises')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/', include(router.urls)),
]
