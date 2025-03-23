from django.urls import path
from . import views 

urlpatterns = [
    path('items/', views.itemCreateview.as_view(), name='itemList'),
    path('items/<str:code>', views.itemDetailView.as_view(), name='itemDetail'),
    path('items/<str:code>/restore/', views.itemRestore.as_view(), name='itemRestore'),
    path('report/<str:item_code>/', views.ReportView.as_view(), name='report'),
]