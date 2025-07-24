from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100, blank=True)  # можно использовать иконки или SVG

    def __str__(self):
        return self.name


class AssetType(models.Model):
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Location(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.address}"


class Listing(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        SOLD = 'sold', _('Sold')
        RESERVED = 'reserved', _('Reserved')
        ARCHIVED = 'archived', _('Archived')

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)
    area = models.PositiveIntegerField(null=True, blank=True, help_text="Площадь (м²)")
    rooms = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.listing.title}"


class Feature(models.Model):
    name = models.CharField(max_length=100)
    listings = models.ManyToManyField(Listing, related_name='features', blank=True)

    def __str__(self):
        return self.name


class ContactRequest(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.user.username} for {self.listing.title}"
