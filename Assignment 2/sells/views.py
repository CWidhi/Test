from rest_framework import generics, status
from rest_framework.response import Response
from .models import SellDetail, SellHeader
from .serializer import SellHeaderSerializer, SellDetailSerializer
from rest_framework.views import APIView


class SellHeaderListCreateView(generics.ListCreateAPIView):
    queryset = SellHeader.objects.filter(is_deleted=False)
    serializer_class = SellHeaderSerializer

class SellHeaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellHeader.objects.filter(is_deleted=False)
    serializer_class = SellHeaderSerializer
    lookup_field = 'code'
    
    def delete(self, request, code):
        try:
            sell_header = SellHeader.objects.get(code=code, is_deleted=False)
            serializer = SellHeaderSerializer()
            serializer.soft_delete(sell_header)
            return Response({"message": "Sell transaction soft deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except SellHeader.DoesNotExist:
            return Response({"error": "Sell transaction not found."}, status=status.HTTP_404_NOT_FOUND)

class RestoreSellHeaderView(APIView):
    def post(self, request, code):
        try:
            sell_header = SellHeader.objects.get(code=code, is_deleted=True)
            serializer = SellHeaderSerializer()
            serializer.restore(sell_header)
            return Response({"message": "Sell transaction restored successfully."}, status=status.HTTP_200_OK)
        except SellHeader.DoesNotExist:
            return Response({"error": "Sell transaction not found."}, status=status.HTTP_404_NOT_FOUND)
        
class SellDetailListCreateView(APIView):
    def get(self, request, header_code):
        details = SellDetail.objects.filter(header_code__code=header_code, is_deleted=False)
        if not details.exists():
            return Response({"error": "No sell details found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, header_code):
        try:
            sell_header = SellHeader.objects.get(code=header_code, is_deleted=False)
        except SellHeader.DoesNotExist:
            return Response({"error": "Sell header not found."}, status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        request_data['header_code'] = header_code 

        serializer = SellDetailSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)