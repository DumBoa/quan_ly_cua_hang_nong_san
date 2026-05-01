# apps/sanpham/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn chính cho trang sản phẩm
    path('quan-ly-san-pham/', views.danh_sach_san_pham, name='danh_sach_san_pham'),
    path('quan-ly-danh-muc-san-pham/', views.quan_ly_danh_muc, name='quan_ly_danh_muc'),
    path('quan-ly-don-vi-tinh/',views.quan_ly_don_vi_tinh, name='quan_ly_don_vi_tinh'),
    
]