from django.db.models import Count
from typing import Any, List, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self,request,queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
    
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1 #min number of items in an order 
    max_num = 10 #max number of items in an order
    extra = 0
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id','customer','payment_status','placed_at']
    list_select_related = ['customer']
    ordering = ['-placed_at']
    # def order_name(self,order):
    #     fn = order.customer_set.first_name
    #     ln = order.customer_set.last_name
    #     return fn + " " + ln


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ['title']
    }
    autocomplete_fields = ['collection']
    search_fields = ['title']
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    #complete list of options: Django Model Admin
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return "Low"
        else:
            return "OK"
    @admin.action(description="Clear Inventory")
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','customer_orders']
    list_editable = ['membership']
    search_fields = ["first_name__istartswith",'last_name__istartswith']
    def customer_orders(self,customer):
        url = (
            reverse('admin:store_order_changelist')
            + "?"
            + urlencode({
                'customer__id': str(customer.id)
            })
               )
        return format_html('<a href = "{}">Orders</a>',url)
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = reverse('admin:store_product_changelist') \
            + '?' \
            + urlencode({
                'collection__id': str(collection.id)
            })
        return format_html('<a href = "{}">{}</a>',url,collection.products_count)
        
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

# Register your models here.



