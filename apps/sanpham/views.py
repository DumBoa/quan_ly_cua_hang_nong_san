# apps/sanpham/views.py
from django.shortcuts import render

def danh_sach_san_pham(request):
    """Hiển thị danh sách sản phẩm"""
    # Dữ liệu mẫu
    san_pham_mau = [
        {'ten': 'Cà chua', 'loai': 'Rau', 'don_vi': 'Kg', 'gia': 20000},
        {'ten': 'Khoai tây', 'loai': 'Củ', 'don_vi': 'Kg', 'gia': 25000},
        {'ten': 'Rau muống', 'loai': 'Rau', 'don_vi': 'Bó', 'gia': 5000},
    ]
    
    context = {
        'san_pham_list': san_pham_mau
    }
    return render(request, 'sanpham/base_sanpham.html', context)

def quan_ly_danh_muc(request):
    """Hiển thị trang quản lý danh mục"""
    return render(request, 'sanpham/qly_danhmuc.html')

def quan_ly_don_vi_tinh(request):
    return render(request, 'sanpham/qly_donvitinh.html')