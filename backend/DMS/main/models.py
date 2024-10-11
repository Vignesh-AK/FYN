from django.db import models

# Create your models here.


class Component(models.Model):
    name = models.CharField(max_length=100)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    STATUS = (
        (1, "Completed"),
        (2, "Pending"),
        (3, "On Hold"),

    )
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS,default=31)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Issue(models.Model):
    STATUS = (
        (1, "Completed"),
        (2, "Pending"),
        (3, "On Hold"),

    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    is_repair = models.BooleanField(default=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=STATUS,default=3)
    issue_description = models.CharField(max_length=250, null=True, blank=True)


    def calculate_total_cost(self):
        return self.component.repair_price if self.is_repair else self.component.new_price

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)
        self.update_vehicle_status()
    
    def update_vehicle_status(self):
        # Check the status of all issues related to the vehicle
        issues = Issue.objects.filter(vehicle=self.vehicle)
        if all(issue.status == 1 for issue in issues):  # All issues are completed
            self.vehicle.status = 1  # Mark the vehicle as 'Completed'
        elif any(issue.status == 3 for issue in issues):  # If any issue is on hold
            self.vehicle.status = 3  # Mark the vehicle as 'On Hold'
        else:
            self.vehicle.status = 2  # Otherwise, keep it 'Pending'
        self.vehicle.save()
    
class Payment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.vehicle} on {self.date}"