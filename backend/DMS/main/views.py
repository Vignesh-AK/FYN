from rest_framework import viewsets, status
from .models import Component, Vehicle, Issue, Payment
from .serializers import ComponentSerializer, IssueSerializer, PaymentSerializer, VehicleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request, *args, **kwargs):
        vehicle_data = request.data
        print(vehicle_data.get('vehicle_id'))
        if vehicle_data.get('vehicle_id'):
            vehicle = Vehicle.objects.get(id=vehicle_data.get('vehicle_id'))
        else:

            vehicle = Vehicle.objects.create(
                make=vehicle_data.get('make'),
                model=vehicle_data.get('model'),
                year=vehicle_data.get('year'),
            )
        
        for issue in vehicle_data.get('issues', []):
            Issue.objects.create(
                vehicle=vehicle,
                component_id=issue['component'],
                issue_description=issue['issue_description'],
            )
        return Response({'message': 'Vehicle and issues created successfully'})

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class VehicleIssuesViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        issues = Issue.objects.filter(vehicle_id=vehicle_id).select_related('component')

        return issues


class VehicleIssueComponentView(APIView):

    def post(self, request):
        data = request.data
        
        # If vehicle ID is provided, fetch existing vehicle
        vehicle_id = data.get('vehicle_id')
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Create new vehicle if ID is not provided
            vehicle_serializer = VehicleSerializer(data={
                'make': data.get('make'),
                'model': data.get('model'),
                'year': data.get('year')
            })
            if vehicle_serializer.is_valid():
                vehicle = vehicle_serializer.save()
            else:
                return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Add issue and component to vehicle
        component_name = data.get('component')
        try:
            component = Component.objects.get(name=component_name)  # Assuming name is unique
        except Component.DoesNotExist:
            return Response({'error': 'Component not found'}, status=status.HTTP_404_NOT_FOUND)

        issue_serializer = IssueSerializer(data={
            'vehicle': vehicle.id,
            'component': component.id,
            'is_repair': data.get('is_repair', True),
            'total_cost': data.get('total_cost')
        })
        if issue_serializer.is_valid():
            issue_serializer.save()
            return Response({'success': 'Vehicle, issue, and component registered successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)