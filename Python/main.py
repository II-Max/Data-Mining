import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
def tool_quet_va_cao_bang():
    print("===> Pandas Web-Catcher <===")
    url = input("1. Nhập URL website: ").strip()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print("\nScaning...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        danh_sach_the_bang = soup.find_all('table')
        if not danh_sach_the_bang:
            print("❌ Không tìm thấy thẻ <table> nào trên trang web này.")
            return None
        print(f"✅ Đã quét thấy {len(danh_sach_the_bang)} bảng dữ liệu.")
        tap_hop_id = set()
        tap_hop_class = set()
        for bang in danh_sach_the_bang:
            if bang.has_attr('id'):
                tap_hop_id.add(bang['id'])
            if bang.has_attr('class'):
                tap_hop_class.add(" ".join(bang['class']))   
        print("\n[ BÁO CÁO TRINH SÁT: CÁC ID TÌM THẤY ]")
        for stt, i in enumerate(tap_hop_id, 1): print(f"  {stt}. {i}")
        if not tap_hop_id: print("  (Không có bảng nào dùng ID)")
        print("\n[ BÁO CÁO TRINH SÁT: CÁC CLASS TÌM THẤY ]")
        for stt, c in enumerate(tap_hop_class, 1): print(f"  {stt}. {c}")
        if not tap_hop_class: print("  (Không có bảng nào dùng Class)")
        print("\n" + "="*50)
        loai_thuoc_tinh = input("2. Bạn muốn dùng 'id' hay 'class' để cào? (Gõ id/class): ").strip().lower()
        ten_thuoc_tinh = input(f"3. Copy dán chính xác tên {loai_thuoc_tinh} từ danh sách trên: ").strip()
        print("\n⏳ Đang cào và tự động làm sạch...")
        danh_sach_bang = pd.read_html(
            io.StringIO(response.text), 
            attrs={loai_thuoc_tinh: ten_thuoc_tinh},
            header=0, thousands=',', decimal='.', na_values=['-', 'N/A', '']
        )
        df_ket_qua = danh_sach_bang[0]
        print(f"\n✅ THÀNH CÔNG! Đã lấy được {len(df_ket_qua)} dòng dữ liệu siêu sạch:")
        print(df_ket_qua.head())
        df_ket_qua.to_csv("du_lieu.csv", index=False, encoding='utf-8-sig')
        print("\n💾 Đã xuất file: du_lieu_quet_tu_dong.csv")
        return df_ket_qua
    except ValueError:
        print(f"\n❌ LỖI: Tên {loai_thuoc_tinh} bạn nhập không khớp với bảng nào.")
    except Exception as e:
        print(f"\n❌ LỖI HỆ THỐNG: {e}")
if __name__ == "__main__":
    df = tool_quet_va_cao_bang()