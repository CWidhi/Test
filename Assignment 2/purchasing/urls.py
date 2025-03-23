from django.urls import path
from . import views

urlpatterns = [
    path('', views.PurchaseHeaderListCreateView.as_view(), name='purchaseListCreate'),
    path('', views.PurchaseHeaderCreateView.as_view(), name='purchaseCreate'),
    path('<str:code>/', views.PurchaseHeaderDetailView.as_view(), name='purchaseDetail'),
    path('<str:code>/restore/', views.PurchaseHeaderRestoreView.as_view(), name='purchaseRestore'),
    path('<str:header_code>/details/', views.PurchaseDetailListCreateView.as_view(), name='purchaseDetailListCreate'),
]
