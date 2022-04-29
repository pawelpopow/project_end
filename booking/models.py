from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    name = models.CharField(max_length=64, null=True)
    gender = models.CharField(max_length=20)
    profile_pic = models.ImageField(
        upload_to="image",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True
    )
    phone_number = models.CharField(max_length=50)
    address = models.TextField()
    state = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.gender


class Rental(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    user = models.ManyToManyField(User, through="Booking")
    name_yacht = models.CharField(max_length=100)
    price = models.DecimalField(default=2000.00, max_digits=7, decimal_places=2)
    is_available = models.BooleanField(default=True)
    yacht_image = models.ImageField(
        upload_to="yacht",
        height_field=None,
        width_field=None,
        max_length=None,
        default='0.jpeg'
    )

    def __str__(self):
        return "Renter: " + str(self.name_yacht)


class Booking(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()
    amount_people = models.PositiveSmallIntegerField()
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.start_day)} : {self.end_day}"
