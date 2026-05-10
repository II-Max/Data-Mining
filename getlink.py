import csv

# Danh sách 63 tỉnh/thành phố trực thuộc trung ương (đã chuẩn hóa chuỗi)
base_domains = [
    "angiang", "bariavungtau", "baclieu", "backan", "bacgiang", "bacninh", "bentre", "binhduong",
    "binhdinh", "binhphuoc", "binhthuan", "camau", "caobang", "cantho", "danang", "daklak",
    "daknong", "dienbien", "dongnai", "dongthap", "gialai", "hagiang", "hanam", "hanoi",
    "hatinh", "haiduong", "haiphong", "haugiang", "hoabinh", "hungyen", "khanhhoa", "kiengiang",
    "kontum", "laichau", "langson", "laocai", "lamdong", "longan", "namdinh", "nghean",
    "ninhbinh", "ninhthuan", "phutho", "phuyen", "quangbinh", "quangnam", "quangngai", "quangninh",
    "quangtri", "soctrang", "sonla", "tayninh", "thaibinh", "thainguyen", "thanhhoa",
    "thuathienhue", "tiengiang", "tphcm", "travinh"
]
# Hậu tố đường dẫn danh bạ
DIRECTORY_PATH = "/danh-ba-dien-tu"

# Tên file xuất ra
output_filename = "danh_ba_chinh_phu.csv"

def generate_directory_links(domains, filename):
    """
    Hàm xử lý danh sách domain và xuất ra file CSV.
    """
    try:
        # Mở file CSV để ghi (write mode)
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Ghi tiêu đề cột (header)
            writer.writerow(["Website_URL"])
            
            # Duyệt qua từng tên miền và tạo link hoàn chỉnh
            for domain in domains:
                # Loại bỏ khoảng trắng thừa nếu có để tránh lỗi cú pháp URL
                clean_domain = domain.strip()
                full_url = f"https://{clean_domain}{DIRECTORY_PATH}"
                
                # Ghi dòng dữ liệu vào file
                writer.writerow([full_url])
                
        print(f"Hoàn thành! Đã xuất {len(domains)} liên kết (link /lɪŋk/) ra tệp '{filename}'.")
        
    except Exception as e:
        print(f"Đã xảy ra lỗi (error /ˈer.ər/) trong quá trình xuất file: {e}")

# Thực thi chương trình
if __name__ == "__main__":
    generate_directory_links(base_domains, output_filename)