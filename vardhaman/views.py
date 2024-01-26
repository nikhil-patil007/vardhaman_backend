from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers  import make_password,check_password

from rest_framework_simplejwt.tokens import RefreshToken  # use to generate Token
from .isAuthanticated import tokenVerified # Custome Class to check Token

import json
import logging

# Models Data here 
from .models import User, Products
from django.db.models import Q
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# Create your views here.

# funtion return the Product Data 
def getProductData(product):
    productObject = {
        "id": product.id,
        "product_image": product.product_image.url if product.product_image else "",
        "product_name_eng": product.product_name_eng if product_name_eng else "" ,
        "product_name_guj": product.product_name_guj if product_name_guj else "",
        "product_name_hin": product.product_name_hin if product_name_hin else "",
        "product_qty": product.product_qty if product.product_qty else "",
        "product_price": product.product_price if f"₹ {product.product_price}" else "₹ 0.00",
        "product_hsn_code": product.product_hsn_code,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }
    return productObject

# function return the User Data
def getUsersData(user):
    userObject = {
        'id' : user.id,
        "name" : user.name if user.name else "",
        "email" : user.email if user.email else "",
        "contact_no" : user.contact_no if user.contact_no else "",
        "is_approved" : user.is_approved if user.is_approved else "",
        "firebase_token" : user.firebase_token if user.firebase_token else "",
        "address" : user.address if user.address else "",
        "role" : user.role if user.role else "",
        'gst_no': user.gst_no if user.gst_no else "",
        "created_at" : user.created_at,
        "updated_at" : user.updated_at
    }
    return userObject

# User Register API
@api_view(["POST"])
def userRegister(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        email = data.get('email')
        contact_no = data.get('contact_no')
        password = data.get('password')
        address = data.get('address')
        firebase_token = data.get('firebase_token')
        if not data:
            return Response({'message':"Please provide valid name, email, contact_no, and password."},status=400)
        
        emailValidate = User.objects.filter(email=email)
        contactValidate = User.objects.filter(contact_no=contact_no)
        if len(emailValidate) > 0 or len(contactValidate) > 0:
            return Response({'message':"User Already Exists."},status=400)
        User.objects.create(
            role = '0',
            name = name,
            email = email,
            contact_no = contact_no,
            password = make_password(password),
            address = address,
            firebase_token = firebase_token,
        )
        return Response({'message':"User register successfully.Wait for Approval."},status=200)
    except json.JSONDecodeError:
        return Response({'message': "Invalid JSON data in the request body."}, status=400)
    except User.DoesNotExist:
        return Response({'message': "User not found."}, status=404)
    except Exception as e:
        logger.error(f"User Register Exception : {str(e)}")
        return Response({'message': str(e)}, status=500)

# User Login API
@api_view(['POST'])
def userLogin(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        firebase_token = data.get('firebase_token')

        if not (username and password):
            return Response({'message': "Please provide a valid username and password."}, status=400)

        email_validate = User.objects.filter(email=username)
        contact_validate = User.objects.filter(contact_no=username)

        if email_validate.exists():
            user_data = email_validate[0]
        elif contact_validate.exists():
            user_data = contact_validate[0]
        else:
            return Response({'message': "User not registered."}, status=404)

        if user_data.is_approved in ('0', '2'):
            return Response({'message': "Access Denied."}, status=403)

        if check_password(password, user_data.password):
            user_data.firebase_token = firebase_token
            user_data.save()
            refresh = RefreshToken.for_user(user_data)
            token = str(refresh.access_token)
            return Response({'message': "User logged in successfully", 'token': token, "userData": getUsersData(user_data)}, status=200)
        else:
            return Response({'message': "Invalid username or password."}, status=400)

    except json.JSONDecodeError:
        return Response({'message': "Invalid JSON data in the request body."}, status=400)
    except User.DoesNotExist:
        return Response({'message': "User not found."}, status=404)
    except Exception as e:
        logger.error(f"User Login Exception: {str(e)}")
        return Response({'message': "Internal server error."}, status=500)

# All Users API
@api_view(['GET'])
@tokenVerified
def getUserDataList(request,userId):
    try:
        if not userId:
            return Response({'message':"Please appropiat User id or all"},status=400)
        
        if userId == "all":
            userData = User.objects.filter(role=0)
        else:
            userData = User.objects.filter(id=userId,role=0).first()
            return Response({'message':"User Data fecthed",'data': getUsersData(userData)},status=200)
        
        userList = []
        for user in userData:
            userValue = getUsersData(user)
            userList.append(userValue)
        return Response({'message':"User Data fecthed",'data': userList},status=200)
    except Exception as e:
        logger.error(f"User Register Exception : {str(e)}")
        return Response({'message': str(e)}, status=500)

# Update User API 
@api_view(['POST'])
@tokenVerified
def userUpdate(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        userId = data.get('userId')
        name = data.get('name')
        email = data.get('email')
        contact_no = data.get('contact_no')
        address = data.get('address')
        gst_no = data.get('gst_no')
        
        userdata = get_object_or_404(User, id=userId)
        userdata.name = name if name else userdata.name
        userdata.email = email if email else userdata.email
        userdata.contact_no = contact_no if contact_no else userdata.contact_no
        userdata.address = address if address else userdata.address
        userdata.gst_no = gst_no if gst_no else userdata.gst_no
        userdata.save() 
        
        return Response({'message': f"Profile Updated successfully"}, status=200)
    except json.JSONDecodeError:
        return Response({'message': "Invalid JSON data in the request body."}, status=400)
    except User.DoesNotExist:
        return Response({'message': "User not found."}, status=404)
    except Exception as e:
        logger.error(f"User Register Exception : {str(e)}")
        return Response({'message': str(e)}, status=500)
        


# User Approval API
@api_view(['POST'])
@tokenVerified
def userApproval(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        userId = data.get('userId')
        approval_status = data.get('approvalStatus')

        if userId is None or approval_status is None:
            return Response({'message': "Please provide valid userId and approvalStatus."}, status=400)

        status_value = {
            "0": ' ',
            "1": ' Approved ',
            "2": ' Rejected ',
        }

        user_instance = get_object_or_404(User, id=userId)
        user_instance.is_approved = approval_status
        user_instance.save()
        return Response({'message': f"User{status_value[approval_status]}successfully"}, status=200)
    except json.JSONDecodeError:
        return Response({'message': "Invalid JSON data in the request body."}, status=400)
    except User.DoesNotExist:
        return Response({'message': "User not found."}, status=404)
    except Exception as e:
        return Response({'message': str(e)}, status=500)

# All Product API
@api_view(['GET'])
@tokenVerified
def getAllProductsList(request):
    try:
        productData = Products.objects.all()
        productList = []
        for product in productData:
            product_data = getProductData(product)
            productList.append(product_data)
        return Response({'message':"Product Data fecthed",'data': productList},status=200)
    except Exception as e:
        logger.error(f"User Register Exception : {str(e)}")
        return Response({'message': str(e)}, status=500)
    
# Product Search API
@api_view(['POST'])
@tokenVerified
def searchProducts(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        productList = []
        
        if not name:
            return Response({"message": "Product Data searched","data": productList},status=200)
            
        productData = Products.objects.filter(
            (Q(product_name_eng__icontains=name) | Q(product_name_guj__icontains=name) | Q(product_name_hin__icontains=name))
        )
        
        for product in productData:
            product_data = getProductData(product)
            productList.append(product_data)
        return Response({'message':"Product Data searched",'data': productList},status=200)
    except json.JSONDecodeError:
        return Response({'message': "Invalid JSON data in the request body."}, status=400)
    except Exception as e:
        logger.error(f"User Register Exception : {str(e)}")
        return Response({'message': str(e)}, status=500)
