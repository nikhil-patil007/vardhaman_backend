from django.db import models

# Create your models here.


class User(models.Model):
    role = models.CharField(max_length=15,default='0',choices=[("0","Customer"),("1","Admin")])
    name = models.CharField(default='',max_length=255,null=True)
    email = models.EmailField(unique=True,max_length=255,null=True)
    contact_no = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255)
    is_approved = models.CharField(max_length=10,default='0',choices=[("0","Pending"),("1","Approved"),("2","Rejected")])
    address = models.CharField(max_length=255,blank=True,null=True)
    firebase_token = models.CharField(max_length=255,blank=True,null=True)
    gst_no = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "users"
    
    def __str__(self):
        return self.name if self.name else self.email
    
class Products(models.Model):
    product_name_eng = models.CharField(max_length=255,null=True)
    product_name_guj = models.CharField(max_length=255,null=True)
    product_name_hin = models.CharField(max_length=255,null=True)
    product_image = models.FileField(upload_to="Product_images/%Y%m%d/%H%M%S/",blank=True,null=True)
    product_qty = models.CharField(max_length=255,null=True)
    product_unit = models.CharField(max_length=255,null=True)
    product_gst_rate = models.IntegerField(default=0)
    product_discount_rate = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_hsn_code = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Products"
        
class Order(models.Model):
    customer_id = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    buyer_name = models.CharField(max_length=255,null=True,blank=True)
    buyer_address = models.CharField(max_length=255,null=True,blank=True)
    buyer_mobile = models.CharField(max_length=255,null=True,blank=True)
    buyer_GST = models.CharField(max_length=255,null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10,default='0',choices=[("0","Pending"),("1","Approved")])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Orders"

class Order_data(models.Model):
    order_id = models.ForeignKey(Order,blank=True,null=True,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,blank=True,null=True,on_delete=models.CASCADE)
    qty = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10,default='0',choices=[("0","Pending"),("1","Approved")])
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Orders_list"
    