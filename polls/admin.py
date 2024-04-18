from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','description', 'content', 'image','date']
    list_filter = ['date']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)