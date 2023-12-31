from django.db import models
from django.core.validators import MinValueValidator
#from django.core.exceptions import ValidationError

# def validate_phone(value):
#     if not 1000000000 <= value <= 9999999999:
#         raise ValidationError(
#             _("%(value)s is not a phone number"),
#             params={"value": value},
#         )

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

    
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    description = models.TextField()
    #max price: $9999.99
    unit_price = models.DecimalField(max_digits=6,
                                      decimal_places=2,
                                      validators = [MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion,blank=True)
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold")
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email  = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)#models.PositiveIntegerField(validators=[validate_phone])
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    class Meta:
        db_table = 'store_customer'
        indexes = [
            models.Index(fields = ["last_name","first_name"])
        ]
        ordering = ['first_name','last_name']

class Order(models.Model):
    STATUS_PENDING = "P"
    STATUS_COMPLETE = "C"
    STATUS_FAILED = "F"
    STATUS_CHOICES = [
        (STATUS_PENDING,"Pending"),
        (STATUS_COMPLETE,"Complete"),
        (STATUS_FAILED,"Failed")
    ]
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    zip = models.CharField(max_length=5,null=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
