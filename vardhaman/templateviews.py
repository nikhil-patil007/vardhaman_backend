from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers  import make_password,check_password
from .models import *
from num2words import num2words
from .views import getProductData, getUsersData
from django.db.models import Q
from django.shortcuts import get_object_or_404
import json
import logging
import ast
import os
from .helpers import sign_indicator

logger = logging.getLogger(__name__)

# this function is returns the amount based on the Number
def getInwordsUsingNumber(amount):
    integer_part = int(amount)
    decimal_part = int((amount - integer_part) * 100)
    integer_words = num2words(integer_part).casefold().replace("-", " ").replace("and", "")
    decimal_words = num2words(decimal_part).casefold().replace("-", " ").replace("and", "")
    return f"{integer_words} rupees and {decimal_words} paise"

# GST counter Function
def calculate_sgst(totalAmount, gstRate):
    gstPrice = (totalAmount * gstRate) / 100
    return gstPrice

# Home Page Path
def index(request):
    if 'userId' in request.session:
        try:
            user_count = User.objects.filter(role='0').count()
            product_count = Products.objects.filter(is_delete='0').count()
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
        users = User.objects.filter(role='0',register_by='self')
        data = {
            'users':users,
            'currentPage':'user',
        }
        return render(request, "allUsers.html",data)
    
    return redirect("login")

# Admin Profile Page Path
def profilePage(request):
    if 'userId' in request.session:
        userData = User.objects.get(id=request.session['userId'])
        data = {
            'userData':userData,
            'currentPage':'profile',
        }
        return render(request, "profile.html",data)
    
    return redirect("login")
    
# All Product Page Path
def productsPage(request):
    if 'userId' in request.session:
        products = Products.objects.filter(is_delete='0').order_by('-id')
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

# All Billing Page Path
def billingPage(request):
    if 'userId' in request.session:
        data = {
            'currentPage': 'orders',
        }
        return render(request, 'billingPage.html', data)
    return redirect('login')

# Invoice Page Path
def invoicePage(request):
    if 'userId' in request.session:
        try:
            orderId = request.POST.get('orderId','')
            orders = Order.objects.get(id=orderId)
            ordersList = Order_data.objects.filter(order_id=orderId, status='1')
            taxes_order = order_taxes.objects.filter(order_id=orderId)
                
            data = {
                'currentPage': 'orders',
                'order': orders,
                'orderList': ordersList,
                'totalAmountWords': getInwordsUsingNumber(orders.total_amount),
                'seller': User.objects.filter(role='1').first(),
                'taxes_order': taxes_order,
            }
            return render(request, 'invoice.html', data)
        except:
            return redirect('ordersPage')
            
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
        
        productGstPrice = calculate_sgst(float(productTaxPrice),float(productGST))
        
        if not productid:
            productdata = Products.objects.create(
                product_name_eng = productNameEng,
                product_name_guj = productNameGuj,
                product_name_hin = productNameHin,
                product_image = productImage,
                product_qty = productQty,
                product_unit = productUnit,
                product_price = productPrice,
                product_gst = productGstPrice,
                product_hsn_code = productHSN,
                product_gst_rate = productGST,
                product_discount_rate = productDiscount,
                product_tax_price = productTaxPrice,
            )
        else:
            product = Products.objects.get(id=productid)
            product.product_name_eng = productNameEng or product.product_name_eng
            product.product_name_guj = productNameGuj or product.product_name_guj
            product.product_name_hin = productNameHin or product.product_name_hin
            product.product_gst_rate = productGST or product.product_gst_rate
            product.product_gst = productGstPrice or product.product_gst
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
    
# Profile Update Functionality
def profileUpdate(request):
    if 'userId' in request.session:
        userData = User.objects.get(id=request.session['userId'])
        userData.shopname = request.POST.get('shopname', '') or userData.shopname
        userData.bankname = request.POST.get('bankName', '') or userData.bankname
        userData.holderName = request.POST.get('holderName', '') or userData.holderName
        userData.ifsc_code = request.POST.get('ifscCode', '') or userData.ifsc_code
        userData.branch_name = request.POST.get('branchName', '') or userData.branch_name
        userData.account_num = request.POST.get('accountNum', '') or userData.account_num
        userData.fassai = request.POST.get('fassai', '') or userData.fassai
        userData.gst_no = request.POST.get('gst', '') or userData.gst_no
        userData.save()
        return redirect('profilePage')
    return redirect("login")    

# Delete Product Path 
def productDeleteFunctionality(request,productId):
    if 'userId' in request.session:
        product = Products.objects.get(id=productId)
        product.is_delete = '1'
        product.save()
        return redirect("productPage")
    
    return redirect("login")    
  
# Login Path
def loginFunction(request):
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # username = username.casefold()

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
    
# This function is count the tax
def process_tax_data(orderId,data):
    processed_data = {}
    orderVal = get_object_or_404(Order,id=orderId)
    for item in data:
        tax_rate = item['tax_rate']
        taxable_amount = float(item['taxable_amount']) + float(item['tax_amount'])
        if tax_rate in processed_data:
            processed_data[tax_rate] += taxable_amount
        else:
            processed_data[tax_rate] = taxable_amount
            
    newList = [{'tax_rate': tax_rate, 'taxable_amount': amount} for tax_rate, amount in processed_data.items()]

    taxable_amount =  0.00
    cgst_amount =  0.00
    sgst_amount =  0.00
    total_tax_amount =  0.00
    
    for i in newList:
        if i['tax_rate'] and i['taxable_amount']:
            orderTax = order_taxes.objects.filter(order_id=orderVal,tax_rate=i['tax_rate'])
            rateCount = product_tax = (float(i['tax_rate']) / 2) # count the tax for cgst and sgst
            gst_cal_amount = calculate_sgst(i['taxable_amount'], rateCount)
            newTaxAmount = float(i['taxable_amount']) - (float(gst_cal_amount) * 2)
            taxable_amount += newTaxAmount
            tax_total_count = float(gst_cal_amount) + float(gst_cal_amount)
            
            cgst_amount += float(gst_cal_amount)
            sgst_amount += float(gst_cal_amount)
            total_tax_amount += float(tax_total_count)
            if not len(orderTax) > 0:
                newo = order_taxes.objects.create(
                    order_id = orderVal,
                    tax_rate = i['tax_rate'],
                    taxable_amount = newTaxAmount,
                    cgst_amount = gst_cal_amount,
                    sgst_amount = gst_cal_amount,
                    total_tax_amount = tax_total_count,
                )
    responseData = {
        "taxable_amount":taxable_amount,
        "cgst_amount":cgst_amount,
        "sgst_amount":sgst_amount,
        "total_tax_amount":total_tax_amount
    }
    
    return responseData


# Function is used to create Bill 
def createOrderFromAdmin(request):
    try:
        if 'userId' in request.session:
            name = request.POST.get('customerName', '')
            mobile = request.POST.get('customerNo', '')
            email = request.POST.get('customerEmail', '').casefold()
            address = request.POST.get('customerAddress', '')
            productList = request.POST.get('productCartItem', '')
            
            listOfProduct = ast.literal_eval(productList)
            
            userData = User.objects.filter(
                name=name,
                contact_no=mobile
            )
            if not len(userData) > 0:
                getUser = User.objects.create(
                    name=name,
                    email=email,
                    contact_no=mobile,
                    address=address,
                    register_by="admin",
                )

            try:
                userdata = get_object_or_404(User, id=request.session['userId'])
            except:
                return redirect('billingPage')
            
            orderId = Order.objects.create(
                customer_id = userdata,
                name = name,
                email = email,
                contact_no = mobile,
                address = address,
                round_off = 0.00,
                total_amount = 0.00,
                grand_total_amount = 0.00,
                status = '1',
            )
            
            price = 0.00
            taxList = []
            
            for i in listOfProduct:
                try:
                    taxObj = {}
                    productdata = get_object_or_404(Products, id=i['product'])
                    amount = float(productdata.product_price) * int(i['qty']) # count the total amount of product
                    product_tax = (float(productdata.product_gst_rate) / 2) # count the tax for cgst and sgst
                    gst_cal_amount = (float(productdata.product_gst) /2 ) * int(i['qty'])  # calculate_sgst(amount, product_tax) # count price with only cgst and sgst
                    tax_amount= (float(gst_cal_amount)*2) + float(amount)
                    price = float(price) + tax_amount
                    
                    taxObj['tax_rate'] = productdata.product_gst_rate
                    taxObj['taxable_amount'] = float(productdata.product_price) * int(i['qty'])
                    taxObj['tax_amount'] = float(productdata.product_gst) * int(i['qty'])
                    taxList.append(taxObj)
                    
                    listing_order = Order_data.objects.create(
                        order_id = orderId,
                        product_id = productdata,
                        qty = i['qty'],
                        cgst_rate = product_tax,
                        sgst_rate = product_tax,
                        cgst_amount = gst_cal_amount,
                        sgst_amount = gst_cal_amount,
                        amount =amount,
                        tax_amount= tax_amount,
                        status = '1',
                    )
                except:
                    pass
                
            taxProcessed = process_tax_data(orderId.id,taxList)
            
            print(taxProcessed)
            totalAmount = float(price)
            sumOrmin = sign_indicator(totalAmount - int(totalAmount))
            
            orderId.round_type = "Less: Rounded Off (+)"
            if sumOrmin:
                orderId.round_type = "Less: Rounded Off (-)"
            
            orderId.taxable_amount = float(taxProcessed['taxable_amount'])
            orderId.cgst_amount = float(taxProcessed['cgst_amount'])
            orderId.sgst_amount = float(taxProcessed['sgst_amount'])
            orderId.total_tax_amount = float(taxProcessed['total_tax_amount'])
            
            orderId.total_amount = totalAmount
            orderId.round_off = totalAmount - int(totalAmount)
            orderId.grand_total_amount = round(totalAmount)
            orderId.save() 
            return redirect('ordersPage')
        else:
            return redirect('login')
    except:
        return redirect('ordersPage')
        
def orderDelete(request,id):
    if 'userId' in request.session:
        orderData = Order.objects.get(id=id)
        orderData.delete()
        return redirect("ordersPage")
    return redirect("login")    
  
    
# Logout path
def logout(request):
    try:
        del request.session['userId']
        return redirect("login")
    except:
        return redirect("login")

# Products search Function 
@csrf_exempt  
def productSearchByName(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            productList = []
            
            if not name:
                return JsonResponse({"data": productList,"status":200})
                
            productData = Products.objects.filter(Q(product_name_eng__icontains=name)).exclude(is_delete='1')
            
            for product in productData:
                product_data = getProductData(product)
                productList.append(product_data)
            
            return JsonResponse({'data': productList,"status":200})
        else:
            return JsonResponse({"message": "Method not allowed",'status':405} )    
    except Exception as e:
        logger.error(f"Product Searching : {str(e)}")
        return JsonResponse({'message': str(e),"status":405})

@csrf_exempt  
def customerSearchByName(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            customerList = []
            
            if not name:
                return JsonResponse({"data": productList,"status":200})
                
            customerData = User.objects.filter(Q(name__icontains=name),role='0').exclude(is_approved='2')
            
            for usr in customerData:
                userValue = getUsersData(usr)
                customerList.append(userValue)
            
            return JsonResponse({'data': customerList,"status":200})
        else:
            return JsonResponse({"message": "Method not allowed",'status':405} )    
    except Exception as e:
        logger.error(f"Customer Searching : {str(e)}")
        return JsonResponse({'message': str(e),"status":405})
        