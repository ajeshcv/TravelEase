from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Image(models.Model):
    url = models.ImageField(upload_to='extra_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description if self.description else 'Image'


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField()
    rating = models.IntegerField(default=5)
    long_description = models.TextField()
    image = models.ImageField(upload_to='places/')
    map_url = models.URLField(max_length=800)
    is_spotlight = models.BooleanField(default=False)
    extra_images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.name


class Spotlight(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='spotlight/')

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('packager', 'Packager'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)
    document = models.FileField(upload_to='packager_documents/', blank=True, null=True)

    def __str__(self):
        return self.username


class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    long_description = models.TextField()
    short_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='packages/main_images/')
    extra_images = models.ManyToManyField('PackageImage', blank=True)  # ManyToManyField for extra images
    packager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'packager'})
    created_at = models.DateTimeField(auto_now_add=True)
    map_url = models.URLField(max_length=700)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class PackageImage(models.Model):
    image = models.ImageField(upload_to='packages/extra_images/')
    description = models.TextField(blank=True, max_length=255)

    def __str__(self):
        return self.description
    

class PackagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="packager_profile")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='packager_profiles/', blank=True, null=True)
    other_details = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    map_url = models.URLField(max_length=700)

    def get_packages(self):
        return Package.objects.filter(packager=self.user)

    def __str__(self):
        return self.name
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    other_details = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Adding location field

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5)


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField()
    rating = models.FloatField(default=0.0)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='hotels/')
    map_url = models.URLField(max_length=800)
    extra_images = models.ManyToManyField('Image', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    payment_link = models.URLField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('paid', 'Paid')],
        default='pending'
    )
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.package.name} by {self.user.username}"

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='pending')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.package.name} by {self.user.username}"


class GalleryImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image by {self.user.username} at {self.uploaded_at}"
    

class FAQ(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faqs', null=True, blank=True) 
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"