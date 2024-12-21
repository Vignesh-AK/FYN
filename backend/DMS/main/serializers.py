from rest_framework import serializers
from .models import Component, Vehicle, Issue, Bill,Service





class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
    
class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Component
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    component = ComponentSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_details = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ['id', 'service', 'total_cost', 'date', 'status', 'status_display', 'service_details']
        read_only_fields = ['date']  # Prevent users from modifying the date

    def get_service_details(self, obj):
        """
        Return essential details about the associated service.
        """
        return {
            "id": obj.service.id,
            "registration_number": obj.service.registration_number,
            "status": obj.service.get_status_display(),
            "total_cost": obj.service.total_cost,
        }


class ServiceSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)
    vehicle = VehicleSerializer(many=False, read_only=True)
    bill = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    
        
    class Meta:
        model = Service
        fields = ['id', 'vehicle', 'total_cost', 'status', 'issue_description', 'registration_number', 'status_display', 'issues', 'bill', 'vehicle']
    def get_bill(self, obj):
        try:
            bill = Bill.objects.get(service=obj)
            return BillSerializer(bill).data
        except Bill.DoesNotExist:
            return None