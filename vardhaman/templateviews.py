from django.shortcuts import render, redirect
from django.contrib.auth.hashers  import make_password,check_password
from .models import *


# Home Page Path
def index(request):
    try:
        if 'userId' in request.session:
            users = User.objects.filter(role='0').count()
            prodcuts = Products.objects.all().count()
            orders = '0'
            data = {
                'users':users,
                'prodcuts':prodcuts,
                'orders':orders,
                'currentPage':'home',
            }
            return render(request, 'index.html',data)
        return redirect("login")
    except:
        return redirect("login")
    
#  Login Page Path
def login(request):
    if 'userId' in request.session:
        return redirect("indexpage")
    return render(request, "Login.html")

# ALL User Page Path
def userPage(request):
    if 'userId' in request.session:
        users = User.objects.filter(role='0')
        data = {
            'users':users,
            'currentPage':'user',
            'currentPage':'user',
        }
        return render(request, "allUsers.html",data)
    return redirect("login")
    
# ALL Product Page Path
def productsPage(request):
    if 'userId' in request.session:
        products = Products.objects.all().order_by('-id')
        data = {
            'products':products,
            'currentPage':'product',
        }
        return render(request, "allProducts.html",data)
    return redirect("login")    

# Add Product Page Path 
def addProductPage(request):
    if 'userId' in request.session:
        data = {
            'currentPage':'product',
        }
        return render(request, "productPage.html",data)
    return redirect("login") 

# Edit Product Page Path   
def editProductPage(request,productId):
    if 'userId' in request.session:
        product = Products.objects.get(id=productId)
        data = {
            'currentPage':'product',
            'productData':product,
        }
        return render(request, "productPage.html",data)
    return redirect("login")    
    
# Add Product funtionality Path
def productAddUpdateFunctionality(request):
    if 'userId' in request.session:
        productid = request.POST.get('productid')
        productNameEng = request.POST.get('productNameEng', '')
        productNameGuj = request.POST.get('productNameGuj', '')
        productNameHin = request.POST.get('productNameHin', '')
        productQty = request.POST.get('productQty', '')
        productPrice = request.POST.get('productPrice', '')
        productHSN = request.POST.get('productHSN', '')
        productImage = request.FILES.get('productImage')

        if not productid:
            productdata = Products.objects.create(
                product_name_eng=productNameEng,
                product_name_guj=productNameGuj,
                product_name_hin=productNameHin,
                product_image=productImage,
                product_qty=productQty,
                product_price=productPrice,
                product_hsn_code=productHSN,
            )
        else:
            product = Products.objects.get(id=productid)
            product.product_name_eng = productNameEng or product.product_name_eng
            product.product_name_guj = productNameGuj or product.product_name_guj
            product.product_name_hin = productNameHin or product.product_name_hin

            if productImage:
                product.product_image = productImage

            product.product_qty = productQty or product.product_qty
            product.product_price = productPrice or product.product_price
            product.product_hsn_code = productHSN or product.product_hsn_code
            product.save()

        return redirect("productPage")
    return redirect("login")    
    
# Delete Product Path 
def productDeleteFunctionality(request,productId):
    if 'userId' in request.session:
        product = Products.objects.get(id=productId)
        product.delete()
        return redirect("productPage")
    return redirect("login")    
    
    
# Login Path
def loginFunction(request):
    try:
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        emailValidation = User.objects.filter(email=username,role='1')
        numberValidataion = User.objects.filter(contact_no=username,role='1')
        if len(emailValidation) > 0:
            userData = emailValidation[0]
        elif len(numberValidataion) > 0:
            userData = numberValidataion[0]
        else:
            msg = "User Doesn't Found"
            userData = ''
        if userData:
            if check_password(password,userData.password):
                request.session['userId']= userData.id
                request.session['userName']= userData.name
                return redirect("indexpage")
            else:
                msg = "Password Incorrect.!"
        return render(request, "Login.html",{'err':msg})
        
    except:
        return redirect("login")

# Logout path
def logout(request):
    try:
        del request.session['userId']
        return redirect("login")
    except:
        return redirect("login")