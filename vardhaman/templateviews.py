from django.shortcuts import render, redirect
from django.contrib.auth.hashers  import make_password,check_password
from .models import *
from num2words import num2words
import logging
logger = logging.getLogger(__name__)

# this function is returns the amount based on the Number
def getInwordsUsingNumber(amount):
    integer_part = int(amount)
    decimal_part = int((amount - integer_part) * 100)
    integer_words = num2words(integer_part).casefold().replace("-", " ").replace("and", "")
    decimal_words = num2words(decimal_part).casefold().replace("-", " ").replace("and", "")
    return f"{integer_words} rupees and {decimal_words} paise"


# Home Page Path
def index(request):
    if 'userId' in request.session:
        try:
            user_count = User.objects.filter(role='0').count()
            product_count = Products.objects.all().count()
            order_count = Order.objects.filter(status='1').count()

            data = {
                'users': user_count,
                'products': product_count,
                'orders': order_count,
                'currentPage': 'home',
            }

            return render(request, 'index.html', data)

        except Exception as e:
            print(f"An error occurred: {e}")
            return redirect('login')
    return redirect('login')
    
# Login Page Path
def login(request):
    if 'userId' in request.session:
        return redirect('indexpage')

    return render(request, 'Login.html')

# All User Page Path
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
    
# All Product Page Path
def productsPage(request):
    if 'userId' in request.session:
        products = Products.objects.all().order_by('-id')
        data = {
            'products': products,
            'currentPage': 'product',
        }
        return render(request, 'allProducts.html', data)

    return redirect('login')    

# All Order Page Path
def ordersPage(request):
    if 'userId' in request.session:
        orders = Order.objects.filter(status='1').order_by('-id')
        data = {
            'orders': orders,
            'currentPage': 'orders',
        }
        return render(request, 'allOrders.html', data)
    return redirect('login')

# Invoice Page Path
def invoicePage(request):
    if 'userId' in request.session:
        # try:
        orderId = request.POST.get('orderId','')
        orders = Order.objects.get(id=orderId)
        ordersList = Order_data.objects.filter(order_id=orderId, status='1')
              
        data = {
            'currentPage': 'orders',
            'order': orders,
            'orderList': ordersList,
            'totalAmountWords': getInwordsUsingNumber(orders.total_amount),
        }
        return render(request, 'invoice.html', data)
        # except:
        #     return redirect('ordersPage')
            
    return redirect('login')
    
# Add Product Page Path 
def addProductPage(request):
    if 'userId' in request.session:
        data = {
            'currentPage' : 'product',
        }
        return render(request, "productPage.html",data)

    return redirect("login") 

# Edit Product Page Path   
def editProductPage(request,productId):
    if 'userId' in request.session:
        product = Products.objects.get(id=productId)
        data = {
            'currentPage' : 'product',
            'productData' : product,
        }
        return render(request, "productPage.html",data)
    
    return redirect("login")    
    
# Add Product funtionality Path
def productAddUpdateFunctionality(request):
    if 'userId' in request.session:
        productid = request.POST.get('productid','')
        productNameEng = request.POST.get('productNameEng', '')
        productNameGuj = request.POST.get('productNameGuj', '')
        productNameHin = request.POST.get('productNameHin', '')
        productQty = request.POST.get('productQty', '')
        productPrice = request.POST.get('productPrice', '')
        productHSN = request.POST.get('productHSN', '')
        productUnit = request.POST.get('productUnit', '')
        productImage = request.FILES.get('productImage')
        productUnit = request.POST.get('productUnit', '')
        productGST = request.POST.get('productGST', '')
        productDiscount = request.POST.get('productDiscount', '')
        productTaxPrice = request.POST.get('productTaxPrice', '')
        
        if not productid:
            productdata = Products.objects.create(
                product_name_eng=productNameEng,
                product_name_guj=productNameGuj,
                product_name_hin=productNameHin,
                product_image=productImage,
                product_qty=productQty,
                product_unit=productUnit,
                product_price=productPrice,
                product_hsn_code=productHSN,
                product_gst_rate=productGST,
                product_discount_rate=productDiscount,
                product_tax_price=productTaxPrice,
            )
        else:
            product = Products.objects.get(id=productid)
            product.product_name_eng = productNameEng or product.product_name_eng
            product.product_name_guj = productNameGuj or product.product_name_guj
            product.product_name_hin = productNameHin or product.product_name_hin
            product.product_gst_rate = productGST or product.product_gst_rate
            product.product_discount_rate = productDiscount or product.product_discount_rate
            product.product_tax_price = productTaxPrice or product.product_tax_price

            if productImage:
                product.product_image = productImage

            product.product_qty = productQty or product.product_qty
            product.product_price = productPrice or product.product_price
            product.product_hsn_code = productHSN or product.product_hsn_code
            product.product_unit = productUnit or product.product_unit
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
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        username = username.casefold()

        email_validation = User.objects.filter(email=username, role='1')
        number_validation = User.objects.filter(contact_no=username, role='1')

        if email_validation.exists():
            user_data = email_validation.first()
        elif number_validation.exists():
            user_data = number_validation.first()
        else:
            return render(request, 'Login.html', {'err': "User not found."})

        if check_password(password, user_data.password):
            request.session['userId'] = user_data.id
            request.session['userName'] = user_data.name
            return redirect('indexpage')
        else:
            return render(request, 'Login.html', {'err': "Incorrect password."})

    except Exception as e:
        # Log the exception or handle it appropriately
        print(f"An error occurred: {e}")
        return redirect('login')

# Logout path
def logout(request):
    try:
        del request.session['userId']
        return redirect("login")
    except:
        return redirect("login")