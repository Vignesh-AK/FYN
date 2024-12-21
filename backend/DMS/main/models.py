from django.db import models

# Create your models here.

class Vehicle(models.Model):
    
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Component(models.Model):
    name = models.CharField(max_length=100)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    

class Service(models.Model):

    STATUS = (
        (1, "Completed"),
        (2, "Pending"),
        (3, "On Hold"),
    )
    
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=STATUS,default=3)
    issue_description = models.CharField(max_length=250, null=True, blank=True)
    registration_number = models.CharField(max_length=255, unique=True)

    def calculate_total_cost(self):
        total_cost = 0
        for issue in self.issues.all():
            total_cost += issue.cost if issue.is_repair else issue.component.new_price
        return total_cost

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        self.total_cost = self.calculate_total_cost()
        self.update_vehicle_status()
    
    def update_vehicle_status(self):
        # Check the status of all issues related to the vehicle
        issues = Issue.objects.filter(service=self)
        
        # Determine the new vehicle status based on the issue statuses
        if all(issue.status == 1 for issue in issues):  # All issues are completed
            self.status = 1  # Mark service status as 'Completed'
        elif any(issue.status == 3 for issue in issues):  # Any issue is on hold
            self.status = 3  # Mark service status as 'On Hold'
        else:
            self.status = 2  # Otherwise, mark service as 'Pending'
        
        # The vehicle status is now calculated dynamically based on related services
        # No need to save vehicle status explicitly, it's dynamically fetched through the Vehicle's status property.

class Issue(models.Model):

    STATUS = (
        (1, "Completed"),
        (2, "Pending"),
        (3, "On Hold"),
    )

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='issues', on_delete=models.CASCADE)
    is_repair = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=STATUS,default=3)
    issue_description = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        if self.is_repair:
            self.cost = self.component.repair_price
        else:
            self.cost = self.component.new_price
        self.service.update_vehicle_status()  # Update vehicle status after saving an issue

class Bill(models.Model):
    STATUS = (
        (1, "Paid"),
        (2, "Not Paid"),
        (3, "On Hold"),
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS,default=3)

    def __str__(self):
        return f"Payment for {self.service.vehicle} on {self.date}"