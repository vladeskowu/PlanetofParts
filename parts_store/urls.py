from . import views
from django.urls import path


app_name = 'parts_store'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-product/', views.add_product, name='add_product'),
    path('about/', views.about, name='about'),
    path('view-cart/', views.view_cart, name='view_cart'),

]
