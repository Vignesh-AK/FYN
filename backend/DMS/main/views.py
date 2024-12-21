from rest_framework import viewsets, status, generics
from .models import Component, Vehicle, Issue, Bill, Service
from .serializers import ComponentSerializer, IssueSerializer, PaymentSerializer, VehicleSerializer, BillSerializer, ServiceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from django.views.decorators.cache import never_cache

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleComponentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ComponentSerializer
    
    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return Component.objects.filter(vehicle_id=vehicle_id)
    
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = PaymentSerializer

class VehicleIssuesViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        issues = Issue.objects.filter(vehicle_id=vehicle_id).select_related('component')

        return issues


class CreateServiceWithIssuesView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract vehicle_id and find the vehicle object
        vehicle_id = data.get("vehicle_id")
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the Service object
        status_code = int(data.get("status", 3))  # Default to Pending (3) if not provided
        issue_description = data.get("issue_description", "")
        registration_number = data.get("registration_number")

        service = Service(
            vehicle=vehicle,
            status=status_code,
            issue_description=issue_description,
            registration_number=registration_number
        )
        service.save()  # Save the service first so it has a primary key value

        # Handle multiple issues and calculate total cost
        issues_data = data.get("issues", [])
        total_cost = Decimal(0)

        for issue_data in issues_data:
            # Extract data for each issue
            component_id = int(issue_data.get("component_id"))
            try:
                component = Component.objects.get(id=component_id)
            except Component.DoesNotExist:
                return Response({"error": f"Component with ID {component_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

            is_repair = bool(issue_data.get("is_repair", True))  # Default to True if not provided
            cost = Decimal(issue_data.get("cost", 0))
            issue_status = int(issue_data.get("status", 3))  # Default to "On Hold" if not provided
            issue_description = issue_data.get("issue_description", "")

            issue = Issue(
                component=component,
                service=service,  # Now the service has a primary key
                is_repair=is_repair,
                cost=cost,
                status=issue_status,
                issue_description=issue_description
            )
            issue.save()

            # Add the issue cost to the service total cost
            total_cost += cost if is_repair else component.new_price

        # Update the total cost of the service
        service.total_cost = total_cost
        service.save()

        # Generate the Bill
        bill = Bill(
            service=service,
            total_cost=total_cost,
            status=2  # Not Paid by default
        )
        bill.save()

        # Return the created service and bill as response
        return Response({
            "message": "Service and Bill created successfully.",
            "service_id": service.id,
            "bill_id": bill.id,
            "total_cost": str(total_cost),
        }, status=status.HTTP_201_CREATED)
    




class BillDetailView(RetrieveAPIView):
    """
    Retrieve bill details.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_field = 'pk'  # or 'id' if you prefer


# Mark bill as paid
class BillPaymentView(APIView):
    """
    Update bill status to 'Paid'.
    """
    def post(self, request, pk):
        try:
            bill = Bill.objects.get(pk=pk)
            if bill.status == 1:
                return Response({"message": "Bill is already marked as paid."}, status=status.HTTP_400_BAD_REQUEST)
            
            bill.status = 1  # Paid
            bill.save()
            return Response({"message": "Bill marked as paid successfully."}, status=status.HTTP_200_OK)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found."}, status=status.HTTP_404_NOT_FOUND)

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()  # Fetch all services
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
class ServiceDetailView(APIView):
    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except Service.DoesNotExist:
            raise Response(detail="Service not found")