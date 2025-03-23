from .models import Items
from .serialize import itemSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime
from sells.models import SellDetail, SellHeader
from purchasing.models import PurchaseDetail
from django.db.models import Sum, F

class itemCreateview(generics.ListCreateAPIView):
    queryset = Items.objects.filter(is_deleted = False)
    serializer_class = itemSerializer
    
class itemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = itemSerializer
    lookup_field = "code"
    
    def get_queryset(self):
        return Items.objects.filter(is_deleted = False)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        
        if "code" in data:
            data.pop("code")
            
        serializer = self.get_serializer(instance, data=data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        item = get_object_or_404(Items, code = kwargs['code'])
        item.is_deleted = True
        item.save()
        return Response({"message": "Item soft deleted"}, status= status.HTTP_204_NO_CONTENT)

class itemRestore(generics.GenericAPIView):
    lookup_field = "code"
    
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Items, code = kwargs['code'])
        if not item.is_deleted:
            return Response({"message:" "Item is already active"}, status=status.HTTP_400_BAD_REQUEST)
        item.is_deleted = False
        item.save()
        return Response({"message": "Item restored succesfully"}, status=status.HTTP_200_OK)

class ReportView(APIView):
    def get(self, request, item_code):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

        item = get_object_or_404(Items, code=item_code)

        # Ambil PurchaseDetail
        purchase_details = PurchaseDetail.objects.filter(
            item_code=item, 
            is_deleted=False,
            created_at__range=[start_date, end_date]
        ).order_by('created_at')

        purchase_summary = purchase_details.aggregate(
            total_in_qty=Sum('quantity'),
            total_in_price=Sum(F('quantity') * F('unit_price'))
        )

        # Ambil SellDetail dan hitung harga berdasarkan PurchaseDetail
        sell_details = SellDetail.objects.filter(
            item_code=item,
            is_deleted=False,
            created_at__range=[start_date, end_date]
        ).order_by('created_at')

        total_out_qty = 0
        total_out_price = 0

        # Hitung total out qty dan total out price berdasarkan PurchaseDetail
        for sell in sell_details:
            purchase_details_for_sell = PurchaseDetail.objects.filter(
                item_code=sell.item_code,
                is_deleted=False
            ).order_by('created_at')

            remaining_quantity = sell.quantity
            for purchase in purchase_details_for_sell:
                available_stock = purchase.quantity
                unit_price = purchase.unit_price

                if remaining_quantity <= 0:
                    break

                if available_stock >= remaining_quantity:
                    total_out_price += remaining_quantity * unit_price
                    total_out_qty += remaining_quantity
                    purchase.quantity -= remaining_quantity
                    remaining_quantity = 0
                else:
                    total_out_price += available_stock * unit_price
                    total_out_qty += available_stock
                    remaining_quantity -= available_stock
                    purchase.quantity = 0

                purchase.save()

        sell_summary = {
            "total_out_qty": total_out_qty,
            "total_out_price": total_out_price
        }

        report = {
            "result": {
                "items": [],
                "item_code": item.code,
                "name": item.name,
                "unit": item.unit,
                "summary": {
                    "in_qty": purchase_summary['total_in_qty'] or 0,
                    "out_qty": sell_summary['total_out_qty'] or 0,
                    "balance_qty": (purchase_summary['total_in_qty'] or 0) - (sell_summary['total_out_qty'] or 0),
                    "balance": (purchase_summary['total_in_price'] or 0) - (sell_summary['total_out_price'] or 0),
                }
            }
        }

        # Tambahkan PurchaseDetail ke laporan
        for purchase in purchase_details:
            report['result']['items'].append({
                "date": purchase.created_at.strftime('%d-%m-%Y'),
                "description": purchase.header_code.description,
                "code": f"P-{purchase.id:03d}",
                "in_qty": purchase.quantity,
                "in_price": purchase.unit_price,
                "in_total": purchase.quantity * purchase.unit_price,
                "out_qty": 0,
                "out_price": 0,
                "out_total": 0,
                "stock_qty": [purchase.quantity],
                "stock_price": [purchase.unit_price],
                "stock_total": [purchase.quantity * purchase.unit_price],
                "balance_qty": (purchase.quantity),
                "balance": (purchase.quantity * purchase.unit_price),
            })
        
        # Tambahkan SellDetail ke laporan
        for sell in sell_details:
            # Calculate unit_price dynamically
            purchase_details_for_sell = PurchaseDetail.objects.filter(
                item_code=sell.item_code,
                is_deleted=False
            ).order_by('created_at')

            remaining_quantity = sell.quantity
            total_price = 0
            unit_price = 0

            for purchase in purchase_details_for_sell:
                available_stock = purchase.quantity
                if remaining_quantity <= 0:
                    break

                if available_stock >= remaining_quantity:
                    unit_price = purchase.unit_price
                    total_price += remaining_quantity * unit_price
                    remaining_quantity = 0
                else:
                    unit_price = purchase.unit_price
                    total_price += available_stock * unit_price
                    remaining_quantity -= available_stock

            report['result']['items'].append({
                "date": sell.created_at.strftime('%d-%m-%Y'),
                "description": sell.header_code.description,
                "code": f"S-{sell.id:03d}",
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": sell.quantity,
                "out_price": unit_price,
                "out_total": total_price,
                "stock_qty": [0],
                "stock_price": [unit_price],
                "stock_total": [total_price],
                "balance_qty": (purchase_summary['total_in_qty'] or 0) - (sell_summary['total_out_qty'] or 0),
                "balance": (purchase_summary['total_in_price'] or 0) - (sell_summary['total_out_price'] or 0),
            })
        
        return JsonResponse(report)




