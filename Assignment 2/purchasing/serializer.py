from rest_framework import serializers
from .models import PurchaseDetail, PurchaseHeader
from items.models import Items

class PurchaseDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source='item_code.code') 
    header_code = serializers.CharField(source='header_code.code')  

    class Meta:
        model = PurchaseDetail
        fields = ["item_code", "quantity", "unit_price", "header_code"] 
    
    def get_details(self, obj):
        active_details = obj.details.filter(is_deleted=False)
        return PurchaseDetailSerializer(active_details, many=True).data
    
    def create(self, validated_data):
        header_code_data = validated_data.pop('header_code') 
        header_code = header_code_data.get('code')  
        
        item_code_data = validated_data.pop('item_code') 
        item_code = item_code_data.get('code')  

        try:
            purchase_header = PurchaseHeader.objects.get(code=header_code)
        except PurchaseHeader.DoesNotExist:
            raise serializers.ValidationError(f"Purchase header with code {header_code} does not exist.")
        
        try:
            item_instance = Items.objects.get(code=item_code) 
        except Items.DoesNotExist:
            raise serializers.ValidationError(f"Item with code {item_code} does not exist.")

        validated_data['item_code'] = item_instance
        validated_data['header_code'] = purchase_header

        purchase_detail = super().create(validated_data)

        item_instance.stock += validated_data['quantity']  
        item_instance.balance += validated_data['unit_price'] * validated_data['quantity']  
        item_instance.save() 

        return purchase_detail

class PurchaseHeaderSerializer(serializers.ModelSerializer): 
    details = PurchaseDetailSerializer(many=True)
    
    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description', 'details']
        
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        purchase_header = PurchaseHeader.objects.create(**validated_data)

        purchase_details = []

        for detail_data in details_data:
            detail_data['header_code'] = purchase_header

            item_code_data = detail_data.pop('item_code') 
            if isinstance(item_code_data, dict):  
                item_code_data = item_code_data.get('code') 

            try:
                item_instance = Items.objects.get(code=item_code_data) 
            except Items.DoesNotExist:
                raise serializers.ValidationError(f"Item with code {item_code_data} does not exist.")

            detail_data['item_code'] = item_instance  
            purchase_detail = PurchaseDetail.objects.create(**detail_data)
            purchase_details.append(purchase_detail)

        for purchase_detail in purchase_details:
            item_instance = purchase_detail.item_code
            item_instance.stock += purchase_detail.quantity 
            item_instance.balance += purchase_detail.unit_price * purchase_detail.quantity 
            item_instance.save() 

        return purchase_header
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data is not None:
            existing_details = {detail.item_code.code: detail for detail in instance.details.all()}
            
            for detail_data in details_data:
                item_code_data = detail_data.pop('item_code')

                if isinstance(item_code_data, dict):
                    item_code_data = item_code_data.get('code')

                try:
                    item_code_instance = Items.objects.get(code=item_code_data)
                except Items.DoesNotExist:
                    raise serializers.ValidationError(f"Item with code {item_code_data} does not exist.")

                if item_code_data in existing_details:
                    existing_detail = existing_details[item_code_data]
                    old_quantity = existing_detail.quantity
                    old_unit_price = existing_detail.unit_price

                    item_code_instance.stock -= old_quantity
                    item_code_instance.balance -= old_unit_price * old_quantity

                    existing_detail.quantity = detail_data.get('quantity', existing_detail.quantity)
                    existing_detail.unit_price = detail_data.get('unit_price', existing_detail.unit_price)
                    existing_detail.save()

                    item_code_instance.stock += existing_detail.quantity
                    item_code_instance.balance += existing_detail.unit_price *  existing_detail.quantity
                    item_code_instance.save()
                else:
                    new_detail = PurchaseDetail.objects.create(
                        header_code=instance,
                        item_code=item_code_instance,
                        **detail_data
                    )

                    item_code_instance.stock += new_detail.quantity
                    item_code_instance.balance += new_detail.unit_price
                    item_code_instance.save()

        return instance

