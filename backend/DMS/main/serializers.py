from rest_framework import serializers
from .models import Component, Vehicle, Issue, Payment

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    component = ComponentSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
    
class VehicleSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'