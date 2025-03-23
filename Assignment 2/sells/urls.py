from django.urls import path
from . import views

urlpatterns = [
    path('', views.SellHeaderListCreateView.as_view(), name='sellListCreate'),
    path('<str:code>/', views.SellHeaderDetailView.as_view(), name='sellDetail'),
    path('<str:code>/restore/', views.RestoreSellHeaderView.as_view(), name='sellRestore'),
    path('<str:header_code>/details/', views.SellDetailListCreateView.as_view(), name='sellDetailViewCreate'),

]
