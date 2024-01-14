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
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_hsn_code = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Products"