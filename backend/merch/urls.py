from django.urls import path

from .views import MerchandiseView, SetStatusView

urlpatterns = [
    path('ambassador/<int:ambassadorId>/merchandise/<int:merchandiseId>/state/',
         SetStatusView.as_view(), name='setstatus')
]
