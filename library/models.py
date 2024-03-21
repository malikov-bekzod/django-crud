from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 60)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to="library/book/")
    count = models.PositiveIntegerField(default = 1)
    last_update = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    ROLES = (
        ('s',"Student"),
        ('t',"Teacher"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length = 20, choices = ROLES, default = ROLES[0])

   

class Booking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    create_date = models.DateField(auto_created = True)

    