from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Customer, Collection, Order, OrderItem
from tags.models import TaggedItem
from itertools import chain

# Create your views here.
def say_hello(request):
    collection = Collection.objects.get(pk=11)
    collection.featured_product = None
    collection.save()

    # taggeditems = TaggedItem.objects.select_related('tag').filter(
    #     content_type=content_type,
    #     object_id=1
    # )
    #select_related: 1 item; prefetch_related: many items
    #queryset = OrderItem.objects.select_related('order','order__customer','product').order_by('order__placed_at')[:5]
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    #result = Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))
    #queryset = Order.objects.select_related('customer').prefetch_related('orderitem__product').order_by('-placed_at')
    #qs1 = Product.objects.filter(collection_id=3)
    #all products with inventory < 10 and price < 20
    #queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)).order_by('unit_price','title')[:5]
    #queryobject = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)).order_by('unit_price','title')[0]
    #queryset = OrderItem.objects.values('product_id','product__title').distinct().order_by('product__title')
    #queryset = Product.objects.filter(id = F('orderitem__product_id')).distinct().order_by('title')
    #queryset = Product.objects.filter(inventory = F('unit_price'))
    #queryset = OrderItem.objects.filter(product__collection_id=3)#chain(Product.objects.filter(collection_id=3), OrderItem.objects.all())
    #queryset = qs1.union(qs2)
    #pk = primary key
    #django queryset api
    return render(request, 'hello.html', {'name':'Ola', 'returned_items':list(queryset)})#'returned_items': list(queryset)})
