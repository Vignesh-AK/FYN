from rest_framework.routers import DefaultRouter
from .views import  *
from django.urls import path

router = DefaultRouter()

router.register(r'vehicles', VehicleViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'vehicles/(?P<vehicle_id>\d+)/components', VehicleComponentViewSet, basename='vehicle-components')

urlpatterns = [
    path('vehicles/<int:vehicle_id>/issues/', VehicleIssuesViewSet.as_view({'get': 'list'}), name='vehicle-issues'),
    path('services/create', CreateServiceWithIssuesView.as_view(), name='vehicle-issue-component'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('bills/<int:pk>/pay/', BillPaymentView.as_view(), name='bill-pay'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service-detail'),


]

urlpatterns += router.urls