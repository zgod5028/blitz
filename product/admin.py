from django.contrib import admin
from .models import (
    AssetCategory, AssetType, Location, Listing,
    ListingImage, Feature, ContactRequest
)

admin.site.register(AssetCategory)
admin.site.register(AssetType)
admin.site.register(Location)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Feature)
admin.site.register(ContactRequest)


