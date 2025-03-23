from rest_framework import generics, status
from rest_framework.response import Response
from .models import PurchaseHeader, PurchaseDetail
from .serializer import PurchaseHeaderSerializer, PurchaseDetailSerializer
from rest_framework.views import APIView

class PurchaseHeaderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer

class PurchaseHeaderCreateView(generics.CreateAPIView):
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer

class PurchaseHeaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer
    lookup_field = 'code'
    
    def delete(self, request, code):
        try:
            purchase_header = PurchaseHeader.objects.get(code=code, is_deleted=False)
            
            for detail in purchase_header.details.all():
                detail.delete()

            purchase_header.is_deleted = True
            purchase_header.save()

            return Response({"message": "Purchase deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except PurchaseHeader.DoesNotExist:
            return Response({"error": "Purchase not found."}, status=status.HTTP_404_NOT_FOUND)

class PurchaseHeaderRestoreView(APIView):
    def post(self, request, code):
        try:
            purchase_header = PurchaseHeader.objects.get(code=code, is_deleted=True)
            purchase_header.restore()
            
            return Response({"message": "Purchase restored successfully."}, status=status.HTTP_200_OK)
        
        except PurchaseHeader.DoesNotExist:
            return Response({"error": "Purchase not found or not deleted."}, status=status.HTTP_404_NOT_FOUND)
        
class PurchaseDetailListCreateView(APIView):
    def get(self, request, header_code):
        details = PurchaseDetail.objects.filter(header_code__code=header_code, is_deleted=False)
        if not details.exists():
            return Response({"error": "No purchase details found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, header_code):
        try:
            purchase_header = PurchaseHeader.objects.get(code=header_code, is_deleted=False)
        except PurchaseHeader.DoesNotExist:
            return Response({"error": "Purchase header not found."}, status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        request_data['header_code'] = header_code 

        serializer = PurchaseDetailSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)