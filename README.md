# Data Mining Suite

Bộ công cụ tổng hợp cho khai thác dữ liệu tự động từ nhiều nguồn:
- **Dữ liệu thời tiết & môi trường**
- **Bài báo nghiên cứu khoa học**
- **Email và bảng dữ liệu trên website**

## 📁 Cấu trúc thư mục

```
Data-Mining/
│
├── Mine_DLThoiTiet/      # Khai thác dữ liệu thời tiết & môi trường
├── Mine_BAIBAONCKH/      # Khai thác bài báo nghiên cứu khoa học
├── Mine_Website/         # Khai thác email & bảng dữ liệu trên website
└── README.md             # (File này)
```

---

## 1. Khai thác dữ liệu thời tiết & môi trường (`Mine_DLThoiTiet`)

- Khai thác dữ liệu khí hậu, môi trường từ NASA Open Data và các nguồn mở.
- Hỗ trợ dữ liệu vệ tinh, thiên văn, khoa học trái đất phục vụ nghiên cứu biến đổi khí hậu, môi trường.
- Tích hợp các dataset lớn, xuất dữ liệu phục vụ phân tích.

**Xem chi tiết:** `Mine_DLThoiTiet/README.md`

---

## 2. Khai thác bài báo nghiên cứu khoa học (`Mine_BAIBAONCKH`)

- Tự động thu thập, xác thực, phân tích bài báo khoa học từ Google Scholar.
- Loại trừ trùng lặp, kiểm tra DOI, phân loại Q, phân tích trích dẫn, tính điểm "hotness".
- Xuất báo cáo chuyên nghiệp dưới dạng Excel phục vụ quản lý nghiên cứu.

**Xem chi tiết:** `Mine_BAIBAONCKH/README.md`

---

## 3. Khai thác email & bảng dữ liệu trên website (`Mine_Website`)

- Quét website để thu thập email và trích xuất bảng dữ liệu HTML.
- Làm sạch, loại trùng, xuất dữ liệu CSV/Excel.
- Kiến trúc module dễ mở rộng, bảo trì.

**Xem chi tiết:** `Mine_Website/README.md`

---

## 🚀 Hướng dẫn sử dụng nhanh

1. **Clone repository:**
```sh
git clone https://github.com/II-Max/Data-Mining.git
cd Data-Mining
```

2. **Cài đặt thư viện cho từng project:**
   - Mỗi thư mục con đều có `requirements.txt` hoặc hướng dẫn cài đặt riêng.
   - Tạo môi trường ảo và cài đặt theo hướng dẫn trong từng README.md.

3. **Chạy từng công cụ khai thác dữ liệu:**
   - Xem file `main.py` và hướng dẫn sử dụng trong từng thư mục con.

---

## 🛠️ Công nghệ sử dụng

- Python 3.8+
- pandas, requests, beautifulsoup4, lxml, openpyxl, rich, ... (xem chi tiết trong từng project)

---

## 📄 License

MIT License

---

## 👤 Tác giả

Phát triển bởi: II-Max và cộng tác viên

---

## ⚠️ Lưu ý pháp lý & đạo đức

Bộ công cụ này chỉ phục vụ mục đích học tập, nghiên cứu, kiểm thử hợp pháp. Người dùng tự chịu trách nhiệm tuân thủ pháp luật và điều khoản website khai thác.

---

> Để biết chi tiết về tính năng, cấu hình và hướng dẫn nâng cao, vui lòng xem README.md trong từng thư mục project.
