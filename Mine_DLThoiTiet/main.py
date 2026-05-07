from numpy import long
import requests
import pandas as pd
import time
def thu_thap_du_lieu_nong_trai_toan_dien():
    try:
        print("\n=> NASA Open Data : AGRI-DATA MINER <=")
        GD = int(input("0. Vĩ Độ - Kinh Độ TP.HN & TP.HCM [0 - 1] : "))
        if(GD == 0):
            print("\n > TP.Hà Nội [ 21.0285° N, 105.8542° E ]")
            print("\n > TP.HCM [ 10.8231° N, 106.6297° E ]")
            print("\n Thời gian : ", time.ctime())
        latitude = float(input("\n 1. Nhập Vĩ độ (Latitude) : ").strip())
        longitude = float(input("\n 2. Nhập Kinh độ (Longitude) [VD: 105.8542]: ").strip())
        khoang_thoi_gian = input("\n 3. Nhập thời gian (YYYYMMDD - YYYYMMDD): ").strip()
        start_date, end_date = [ngay.strip() for ngay in khoang_thoi_gian.split('-')]
        
        danh_sach_thong_so = "T2M,TS,PRECTOTCORR,RH2M,WS10M,ALLSKY_SFC_SW_DWN"
        
        url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        
        tham_so = {
            "parameters": danh_sach_thong_so,
            "community": "AG",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }
        
        print(f"\n⏳ Đang kết nối NASA tải tổ hợp dữ liệu nông nghiệp...")
        response = requests.get(url, params=tham_so, timeout=20)
        response.raise_for_status()
        
        data_json = response.json()['properties']['parameter']
        df = pd.DataFrame(data_json)
        
        df = df.reset_index().rename(columns={'index': 'Mốc thời gian'})
        df['Mốc thời gian'] = pd.to_datetime(df['Mốc thời gian'], format='%Y%m%d%H').dt.strftime('%Y-%m-%d %H:00')
        
        df = df.rename(columns={
            'T2M': 'Nhiệt độ KK (°C)',
            'TS': 'Nhiệt độ Đất (°C)',
            'PRECTOTCORR': 'Lượng mưa (mm)',
            'RH2M': 'Độ ẩm (%)',
            'WS10M': 'Gió (m/s)',
            'ALLSKY_SFC_SW_DWN': 'Bức xạ MT (W/m²)'
        })
        
        print(f"\n✅ THÀNH CÔNG! (Hiển thị 5 giờ đầu tiên):")
        print(df.head())
        
        ten_file = f"AgriData_{start_date}_{end_date}_{latitude}_{longitude}.csv"
        df.to_csv(ten_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 Đã lưu bộ dữ liệu nông trại vào: {ten_file}")
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")

if __name__ == "__main__":
    thu_thap_du_lieu_nong_trai_toan_dien()