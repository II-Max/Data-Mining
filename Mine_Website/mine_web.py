import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import re

def scrape_all_tables(response_text):
    print("\n⏳ Đang cào và tự động làm sạch tất cả các bảng...")
    try:
        # Sử dụng pandas để tự động tìm và trích xuất tất cả các thẻ <table>
        danh_sach_bang = pd.read_html(
            io.StringIO(response_text), 
            header=0, thousands=',', decimal='.', na_values=['-', 'N/A', '']
        )
        
        if not danh_sach_bang:
            print("❌ Không tìm thấy hoặc không thể đọc bảng nào trên trang này.")
            return []
            
        print(f"\n✅ THÀNH CÔNG! Đã lấy được {len(danh_sach_bang)} bảng dữ liệu.")
        for idx, df in enumerate(danh_sach_bang):
            print(f"\n--- Bảng {idx + 1} ({len(df)} dòng) ---")
            print(df.head())
            file_name = f"du_lieu_bang_{idx + 1}.csv"
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"💾 Đã xuất file: {file_name}")
            
        return danh_sach_bang
    except ValueError:
        print("\n❌ Không tìm thấy bảng nào có định dạng phù hợp để đọc.")
        return []

def mine_emails(response_text):
    print("\n⏳ Đang quét toàn bộ dữ liệu trang web để tìm email...")
    # Biểu thức chính quy (Regex) để tìm cấu trúc email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = set(re.findall(email_pattern, response_text))
    
    if emails:
        print(f"\n✅ Đã tìm thấy {len(emails)} email:")
        for stt, email in enumerate(emails, 1):
            print(f"  {stt}. {email}")
            
        df_emails = pd.DataFrame(list(emails), columns=['Email'])
        df_emails.to_csv("danh_sach_email.csv", index=False, encoding='utf-8-sig')
        print("💾 Đã xuất file: danh_sach_email.csv")
    else:
        print("\n❌ Không tìm thấy bất kỳ email nào trên trang này.")

def main():
    print("===> Data Miner - Tự động hóa <===")
    url = input("1. Nhập URL website cần quét: ").strip()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print("\n⏳ Đang kết nối tới website...")
        response = requests.get(url, headers=headers, timeout=10)
        
        while True:
            print("\n" + "="*50)
            print("CÁC CHỨC NĂNG MINING:")
            print("1. Tự động cào TẤT CẢ các bảng và lưu thành CSV")
            print("2. Quét và trích xuất danh sách Email")
            print("3. Thoát")
            lua_chon = input("Chọn chức năng (1/2/3): ").strip()
            
            if lua_chon == '1':
                scrape_all_tables(response.text)
            elif lua_chon == '2':
                # Tìm email qua text thuần để sạch hơn và tìm trong toàn bộ phản hồi HTML (raw text) để bắt các email ẩn.
                mine_emails(response.text)
            elif lua_chon == '3':
                print("Đang thoát chương trình...")
                break
            else:
                print("❌ Lựa chọn không hợp lệ, vui lòng chọn lại.")
                
    except requests.exceptions.RequestException as e:
        print(f"\n❌ LỖI KẾT NỐI: Không thể truy cập URL. Chi tiết: {e}")
    except Exception as e:
        print(f"\n❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    main()
