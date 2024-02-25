from django.urls import path

from .views import MerchandiseView, SetStatusView


urlpatterns = [
    path('api/merchandise', MerchandiseView.as_view({'get': 'list'}),
         name='merchandise'),
    path('api/ambassadors/<int:ambassadorId>/merchandise/<int:merchandiseId>/state',  # noqa
         SetStatusView.as_view(), name='setstatus')
]
