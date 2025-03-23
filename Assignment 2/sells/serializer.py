from rest_framework import serializers
from .models import SellDetail, SellHeader
from items.models import Items
from purchasing.models import PurchaseDetail

class SellDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source = 'item_code.code')
    header_code = serializers.CharField(source= 'header_code.code')
    
    class Meta:
        model = SellDetail
        fields = ["item_code", "quantity", "header_code"] 
        
    def get_details(self, obj):
        active_details = obj.details.filter(is_deleted=False)
        return SellDetailSerializer(active_details, many=True).data
    
    def create(self, validated_data):
        header_code = validated_data.pop('header_code')['code']
        item_code = validated_data.pop('item_code')['code']
        quantity_needed = validated_data['quantity']

        try:
            sell_header = SellHeader.objects.get(code=header_code, is_deleted=False)
        except SellHeader.DoesNotExist:
            raise serializers.ValidationError(f"Sell header with code {header_code} does not exist.")

        try:
            item_instance = Items.objects.get(code=item_code)
        except Items.DoesNotExist:
            raise serializers.ValidationError(f"Item with code {item_code} does not exist.")

        purchase_details = PurchaseDetail.objects.filter(
            item_code=item_instance, is_deleted=False
        ).order_by('id') 

        if not purchase_details.exists():
            raise serializers.ValidationError(f"No stock available for item {item_code}.")

        total_balance_reduction = 0
        remaining_quantity = quantity_needed

        for purchase in purchase_details:
            if remaining_quantity <= 0:
                break 

            available_stock = purchase.quantity
            unit_price = purchase.unit_price

            if available_stock >= remaining_quantity:
                total_balance_reduction += remaining_quantity * unit_price
                purchase.quantity -= remaining_quantity
                remaining_quantity = 0
            else:
                total_balance_reduction += available_stock * unit_price
                remaining_quantity -= available_stock
                purchase.quantity = 0

            purchase.save()

        if remaining_quantity > 0:
            raise serializers.ValidationError(f"Insufficient stock for item {item_code}.")

        item_instance.stock -= quantity_needed
        item_instance.balance -= total_balance_reduction
        item_instance.save()

        validated_data['item_code'] = item_instance
        validated_data['header_code'] = sell_header
        return super().create(validated_data)
    

class SellHeaderSerializer(serializers.ModelSerializer):
    details = SellDetailSerializer(many= True)
    
    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description', 'details']
        
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        sell_header = SellHeader.objects.create(**validated_data)

        for detail_data in details_data:
            item_code_data = detail_data.pop('item_code')
            if isinstance(item_code_data, dict):
                item_code_data = item_code_data.get('code')

            purchase_details = PurchaseDetail.objects.filter(
                item_code__code=item_code_data, is_deleted=False
            ).order_by('-unit_price')

            if not purchase_details.exists():
                raise serializers.ValidationError(f"Item with code {item_code_data} has no stock available.")

            total_quantity_needed = detail_data['quantity']
            total_balance_reduction = 0
            remaining_quantity = total_quantity_needed

            for purchase in purchase_details:
                if remaining_quantity <= 0:
                    break

                available_stock = purchase.quantity  

                if available_stock >= remaining_quantity:
                    total_balance_reduction += remaining_quantity * purchase.unit_price
                    purchase.quantity -= remaining_quantity 
                    remaining_quantity = 0
                else:
                    total_balance_reduction += available_stock * purchase.unit_price
                    remaining_quantity -= available_stock
                    purchase.quantity = 0  

                purchase.save()  

            if remaining_quantity > 0:
                raise serializers.ValidationError(f"Insufficient stock for item {item_code_data}.")

            item_instance = Items.objects.get(code=item_code_data)
            item_instance.stock -= total_quantity_needed
            item_instance.balance -= total_balance_reduction
            item_instance.save()

            detail_data['item_code'] = item_instance
            detail_data['header_code'] = sell_header
            SellDetail.objects.create(**detail_data)


            return sell_header
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data is not None:
            for old_detail in instance.details.all():
                item_instance = old_detail.item_code
                item_instance.stock += old_detail.quantity  
                purchase_details = PurchaseDetail.objects.filter(
                    item_code=item_instance, is_deleted=False
                ).order_by('-unit_price')

                total_balance_add = 0
                remaining_quantity = old_detail.quantity

                for purchase in purchase_details:
                    if remaining_quantity <= 0:
                        break
                    available_stock = purchase.quantity
                    if available_stock >= remaining_quantity:
                        total_balance_add += remaining_quantity * purchase.unit_price
                        remaining_quantity = 0
                    else:
                        total_balance_add += available_stock * purchase.unit_price
                        remaining_quantity -= available_stock

                item_instance.balance += total_balance_add 
                item_instance.save()
                old_detail.delete()

            for detail_data in details_data:
                item_code_data = detail_data.pop('item_code')
                if isinstance(item_code_data, dict):
                    item_code_data = item_code_data.get('code')

                purchase_details = PurchaseDetail.objects.filter(
                    item_code__code=item_code_data, is_deleted=False
                ).order_by('-unit_price')

                if not purchase_details.exists():
                    raise serializers.ValidationError(f"Item with code {item_code_data} has no stock available.")

                total_quantity_needed = detail_data['quantity']
                total_balance_reduction = 0
                remaining_quantity = total_quantity_needed

                for purchase in purchase_details:
                    if remaining_quantity <= 0:
                        break

                    available_stock = purchase.quantity
                    if available_stock >= remaining_quantity:
                        total_balance_reduction += remaining_quantity * purchase.unit_price
                        remaining_quantity = 0
                    else:
                        total_balance_reduction += available_stock * purchase.unit_price
                        remaining_quantity -= available_stock

                if remaining_quantity > 0:
                    raise serializers.ValidationError(f"Insufficient stock for item {item_code_data}.")

                item_instance = Items.objects.get(code=item_code_data)
                item_instance.stock -= total_quantity_needed
                item_instance.balance -= total_balance_reduction
                item_instance.save()

                detail_data['item_code'] = item_instance
                detail_data['header_code'] = instance
                SellDetail.objects.create(**detail_data)

        return instance
    
    def soft_delete(self, instance):
        if not instance.is_deleted:
            instance.is_deleted = True
            instance.save()

            for detail in instance.details.all():
                item_instance = detail.item_code
                item_instance.stock += detail.quantity 

                purchase_details = PurchaseDetail.objects.filter(
                    item_code=item_instance, is_deleted=False
                ).order_by('-unit_price')

                total_balance_add = 0
                remaining_quantity = detail.quantity

                for purchase in purchase_details:
                    if remaining_quantity <= 0:
                        break

                    available_stock = purchase.quantity
                    if available_stock >= remaining_quantity:
                        total_balance_add += remaining_quantity * purchase.unit_price
                        remaining_quantity = 0
                    else:
                        total_balance_add += available_stock * purchase.unit_price
                        remaining_quantity -= available_stock

                item_instance.balance += total_balance_add  
                item_instance.save()

                detail.is_deleted = True
                detail.save()
                
    def restore(self, instance):
        if instance.is_deleted:
            instance.is_deleted = False
            instance.save()

            for detail in instance.details.all():
                item_instance = detail.item_code
                item_instance.stock -= detail.quantity  

                purchase_details = PurchaseDetail.objects.filter(
                    item_code=item_instance, is_deleted=False
                ).order_by('-unit_price')

                total_balance_reduction = 0
                remaining_quantity = detail.quantity

                for purchase in purchase_details:
                    if remaining_quantity <= 0:
                        break

                    available_stock = purchase.quantity
                    if available_stock >= remaining_quantity:
                        total_balance_reduction += remaining_quantity * purchase.unit_price
                        remaining_quantity = 0
                    else:
                        total_balance_reduction += available_stock * purchase.unit_price
                        remaining_quantity -= available_stock

                item_instance.balance -= total_balance_reduction  
                item_instance.save()

            detail.is_deleted = False
            detail.save()