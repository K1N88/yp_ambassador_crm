from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AmbassadorsViewSet, BudgetViewSet, StudyProgrammViewSet,
                       SupervisorViewSet, ContentViewSet, import_ambassadors)
from merch.views import MerchandiseView, SetStatusView

router = DefaultRouter()

router.register(r'ambassadors', AmbassadorsViewSet, basename='ambassadors')
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'supervisors', StudyProgrammViewSet)
router.register(r'study_programms', SupervisorViewSet)
router.register(r'merchandise', MerchandiseView, basename='merchandises')
router.register(r'content', ContentViewSet, basename='content')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/ambassadors/import/', import_ambassadors,
         name='import_ambassadors'),
    path('api/ambassadors/<int:ambassadorId>/merchandise/<int:merchandiseId>/state',  # noqa
         SetStatusView.as_view(), name='setstatus'),
    path('api/', include(router.urls)),
]
