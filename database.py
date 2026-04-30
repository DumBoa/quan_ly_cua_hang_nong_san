# database.py
import sqlite3

DB_NAME = "cuahangnongsan.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    -- ========================
    -- 1. DANH MỤC & SẢN PHẨM
    -- ========================
    CREATE TABLE IF NOT EXISTS danh_muc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        id_cha INTEGER,
        mo_ta TEXT,
        FOREIGN KEY (id_cha) REFERENCES danh_muc(id)
    );

    CREATE TABLE IF NOT EXISTS don_vi_tinh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS san_pham (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        id_danh_muc INTEGER,
        id_don_vi INTEGER,
        ma_vach TEXT UNIQUE,
        ma_qr TEXT,
        mo_ta TEXT,
        hinh_anh TEXT,
        xuat_xu TEXT,
        thuong_hieu TEXT,
        can_nang_mac_dinh REAL,
        ton_kho_toi_thieu REAL,
        trang_thai TEXT DEFAULT 'hoat_dong',
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_danh_muc) REFERENCES danh_muc(id),
        FOREIGN KEY (id_don_vi) REFERENCES don_vi_tinh(id)
    );

    -- ========================
    -- 2. GIÁ & KHUYẾN MÃI
    -- ========================
    CREATE TABLE IF NOT EXISTS gia_san_pham (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_san_pham INTEGER,
        loai_gia TEXT CHECK(loai_gia IN ('le', 'si')),
        gia REAL NOT NULL,
        ngay_bat_dau DATETIME,
        ngay_ket_thuc DATETIME,
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );

    CREATE TABLE IF NOT EXISTS khuyen_mai (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT,
        phan_tram_giam REAL,
        ngay_bat_dau DATETIME,
        ngay_ket_thuc DATETIME
    );

    CREATE TABLE IF NOT EXISTS khuyen_mai_san_pham (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_khuyen_mai INTEGER,
        id_san_pham INTEGER,
        FOREIGN KEY (id_khuyen_mai) REFERENCES khuyen_mai(id),
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );

    CREATE TABLE IF NOT EXISTS combo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT,
        gia_combo REAL
    );

    CREATE TABLE IF NOT EXISTS chi_tiet_combo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_combo INTEGER,
        id_san_pham INTEGER,
        so_luong INTEGER,
        FOREIGN KEY (id_combo) REFERENCES combo(id),
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );

    -- ========================
    -- 3. NHÂN VIÊN
    -- ========================
    CREATE TABLE IF NOT EXISTS vai_tro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT
    );

    CREATE TABLE IF NOT EXISTS nhan_vien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT,
        so_dien_thoai TEXT,
        email TEXT,
        id_vai_tro INTEGER,
        trang_thai TEXT DEFAULT 'hoat_dong',
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_vai_tro) REFERENCES vai_tro(id)
    );

    CREATE TABLE IF NOT EXISTS lich_lam_viec (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nhan_vien INTEGER,
        ngay DATE,
        gio_bat_dau TIME,
        gio_ket_thuc TIME,
        FOREIGN KEY (id_nhan_vien) REFERENCES nhan_vien(id)
    );

    -- ========================
    -- 4. NHÀ CUNG CẤP & NHẬP
    -- ========================
    CREATE TABLE IF NOT EXISTS nha_cung_cap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT,
        so_dien_thoai TEXT,
        email TEXT,
        dia_chi TEXT,
        danh_gia INTEGER,
        trang_thai TEXT DEFAULT 'hop_tac',
        ghi_chu TEXT
    );

    CREATE TABLE IF NOT EXISTS phieu_nhap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ncc INTEGER,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        tong_tien REAL,
        trang_thai TEXT DEFAULT 'da_nhap',
        ghi_chu TEXT,
        FOREIGN KEY (id_ncc) REFERENCES nha_cung_cap(id)
    );

    CREATE TABLE IF NOT EXISTS chi_tiet_nhap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_phieu_nhap INTEGER,
        id_san_pham INTEGER,
        so_luong REAL,
        gia_nhap REAL,
        han_su_dung DATE,
        ma_lo TEXT,
        FOREIGN KEY (id_phieu_nhap) REFERENCES phieu_nhap(id),
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );

    -- ========================
    -- 5. KHO
    -- ========================
    CREATE TABLE IF NOT EXISTS kho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT
    );

    CREATE TABLE IF NOT EXISTS ton_kho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_san_pham INTEGER,
        id_kho INTEGER,
        ma_lo TEXT,
        so_luong REAL,
        han_su_dung DATE,
        ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id),
        FOREIGN KEY (id_kho) REFERENCES kho(id)
    );

    CREATE TABLE IF NOT EXISTS lich_su_kho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_san_pham INTEGER,
        id_kho INTEGER,
        loai TEXT CHECK(loai IN ('nhap', 'xuat', 'chuyen', 'dieu_chinh', 'huy')),
        so_luong REAL,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        id_tham_chieu INTEGER,
        ghi_chu TEXT
    );

    -- ========================
    -- 6. KHÁCH HÀNG & BÁN
    -- ========================
    CREATE TABLE IF NOT EXISTS khach_hang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT,
        so_dien_thoai TEXT,
        email TEXT,
        dia_chi TEXT,
        loai TEXT CHECK(loai IN ('thuong', 'vip')),
        diem INTEGER DEFAULT 0,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS hoa_don (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_khach_hang INTEGER,
        id_nhan_vien INTEGER,
        trang_thai TEXT CHECK(trang_thai IN ('tam', 'hoan_thanh', 'huy')),
        tong_tien REAL,
        giam_gia REAL DEFAULT 0,
        tong_thanh_toan REAL,
        ghi_chu TEXT,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_khach_hang) REFERENCES khach_hang(id),
        FOREIGN KEY (id_nhan_vien) REFERENCES nhan_vien(id)
    );

    CREATE TABLE IF NOT EXISTS chi_tiet_hoa_don (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_hoa_don INTEGER,
        id_san_pham INTEGER,
        so_luong REAL,
        gia REAL,
        giam_gia REAL DEFAULT 0,
        FOREIGN KEY (id_hoa_don) REFERENCES hoa_don(id),
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );

    -- ========================
    -- 7. THANH TOÁN
    -- ========================
    CREATE TABLE IF NOT EXISTS thanh_toan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_hoa_don INTEGER,
        phuong_thuc TEXT CHECK(phuong_thuc IN ('tien_mat', 'chuyen_khoan')),
        so_tien REAL,
        trang_thai TEXT DEFAULT 'hoan_tat',
        ma_giao_dich TEXT,
        ngay_thanh_toan DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_hoa_don) REFERENCES hoa_don(id)
    );

    CREATE TABLE IF NOT EXISTS hoan_tien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_hoa_don INTEGER,
        so_tien REAL,
        ly_do TEXT,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_hoa_don) REFERENCES hoa_don(id)
    );

    -- ========================
    -- 8. KIỂM KÊ
    -- ========================
    CREATE TABLE IF NOT EXISTS kiem_ke (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_kho INTEGER,
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_kho) REFERENCES kho(id)
    );

    CREATE TABLE IF NOT EXISTS chi_tiet_kiem_ke (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_kiem_ke INTEGER,
        id_san_pham INTEGER,
        so_luong_he_thong REAL,
        so_luong_thuc_te REAL,
        chenh_lech REAL,
        FOREIGN KEY (id_kiem_ke) REFERENCES kiem_ke(id),
        FOREIGN KEY (id_san_pham) REFERENCES san_pham(id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Tạo database và bảng thành công!")