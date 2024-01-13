from django.urls import path
from . import views

urlpatterns = [
    path('api/user_register',views.userRegister),
    path('api/user_login',views.userLogin),
    path('api/fetch_user_data_list/<str:userId>',views.getUserDataList),
    path('api/user_approval_by_admin',views.userApproval),
    path('api/get_all_product_list',views.getAllProductsList),
    path('api/search_product_list',views.searchProducts),
]
