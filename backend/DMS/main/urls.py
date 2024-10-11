from rest_framework.routers import DefaultRouter
from .views import  ComponentViewSet, IssueViewSet, PaymentViewSet, VehicleIssuesViewSet, VehicleViewSet, VehicleIssueComponentView
from django.urls import path

router = DefaultRouter()

router.register(r'vehicles', VehicleViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('vehicles/<int:vehicle_id>/issues/', VehicleIssuesViewSet.as_view({'get': 'list'}), name='vehicle-issues'),
    path('vehicles/register/', VehicleIssueComponentView.as_view(), name='vehicle-issue-component'),

]

urlpatterns += router.urls