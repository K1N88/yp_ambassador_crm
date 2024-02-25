from django.urls import path

from .views import MerchandiseView, SetStatusView

urlpatterns = [
    path('api/merchandise', MerchandiseView.as_view({'get': 'list'}), name='merchandise'),
    path('ambassador/<int:ambassadorId>/merchandise/<int:merchandiseId>/state',
         SetStatusView.as_view(), name='setstatus')
]
