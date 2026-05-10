# 📚 Scientific Research Miner - Hệ Thống Khai Thác Công Bố Khoa Học

> **Công cụ chuyên nghiệp để khai thác, xác thực và phân tích các công bố khoa học từ Google Scholar**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

---

## 📖 Mục Lục

- [Tổng Quan](#tổng-quan)
- [Tính Năng Chính](#tính-năng-chính)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Cấu Hình](#cấu-hình)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Chi Tiết Các Module](#chi-tiết-các-module)
- [Kết Quả Xuất Ra](#kết-quả-xuất-ra)
- [Các Tính Năng Nâng Cao](#các-tính-năng-nâng-cao)
- [Xử Lý Lỗi & Khắc Phục](#xử-lý-lỗi--khắc-phục)
- [FAQ & Hỏi Đáp](#faq--hỏi-đáp)

---

## 🎯 Tổng Quan

**Scientific Research Miner** là một hệ thống tự động hóa toàn diện để:
- **Khai thác** hàng chục đến hàng trăm công bố khoa học từ Google Scholar
- **Xác thực** dữ liệu bằng kiểm tra trùng lặp, định dạng DOI, và các tiêu chí chất lượng
- **Phân tích** các bài báo theo hạng Q, tần suất trích dẫn, và độ "nóng" (hotness score)
- **Xuất báo cáo** chuyên nghiệp dưới dạng Excel với tóm tắt điều hành

Dự án sử dụng **kiến trúc module hóa** để dễ bảo trì, mở rộng và kiểm thử. Mỗi bước xử lý (khai thác → xác thực → định dạng) là một module độc lập với trách nhiệm rõ ràng.

---

## ✨ Tính Năng Chính

### 🔍 Khai Thác Dữ Liệu (Mining)
- ✅ Tích hợp API Google Scholar qua SerpApi
- ✅ Hỗ trợ lọc theo **hạng tạp chí**: Nature, Science, IEEE, ACM, Cell (top-tier)
- ✅ Lọc theo **năm xuất bản** (mặc định từ 2020)
- ✅ **Retry logic** với exponential backoff (tối đa 3 lần)
- ✅ **Rate limiting** có thể cấu hình (1 request/giây mặc định)
- ✅ Timeout có thể cấu hình (30 giây mặc định)

### ✔️ Xác Thực Dữ Liệu (Validation)
- ✅ Xóa các **bản ghi trùng lặp** theo tiêu đề
- ✅ **Kiểm tra định dạng DOI** (Digital Object Identifier)
- ✅ **Chuẩn hóa** tiêu đề, tác giả, tạp chí
- ✅ **Lọc theo số trích dẫn** tối thiểu (configurable)
- ✅ **Xác thực kiểu dữ liệu**: năm, số trích dẫn, độ "nóng"

### 📊 Định Dạng & Xuất Ra (Formatting)
- ✅ **Báo cáo Excel** với 3 sheet:
  - **Executive Summary**: Tóm tắt chất lượng với quality score (0-100)
  - **Insights**: Những phát hiện chính (tạp chí hàng đầu, bài báo nóng nhất)
  - **Clean Data**: Dữ liệu đầy đủ có thể lọc và sắp xếp
- ✅ **Tính điểm chất lượng** dựa trên:
  - Tỷ lệ bài báo Q1/Q2 (hạng tạp chí)
  - Tỷ lệ bài báo gần đây (2 năm gần nhất)
  - Độ bao phủ DOI
  - Độ "nóng" trung bình (citations/year)

### 🛡️ Bảo Mật & Độ Tin Cậy
- ✅ **Không hardcode** thông tin nhạy cảm (API key lưu trong .env)
- ✅ **Xử lý lỗi toàn diện** với thông báo chi tiết
- ✅ **Logging có cấu trúc** (file + console output)
- ✅ **Input validation** trên tất cả tham số đầu vào
- ✅ **Graceful degradation** khi API không khả dụng

### ⚡ Tối Ưu Hóa
- ✅ **Xử lý song song** có thể được thêm vào (async/await ready)
- ✅ **Caching có thể** được triển khai cho các truy vấn lặp lại
- ✅ **Tối ưu hóa bộ nhớ** cho xử lý dataset lớn

---

## 💻 Yêu Cầu Hệ Thống

### Phần Cứng
- **CPU**: Dual-core tối thiểu
- **RAM**: 2GB tối thiểu (4GB khuyến cáo)
- **Ổ cứng**: 100MB cho log và output

### Phần Mềm
```
Python:           3.8+ (3.10+ khuyến cáo)
Hệ điều hành:     Windows, macOS, Linux
API Key:          SerpApi (miễn phí tại https://serpapi.com/)
Kết nối Internet: Bắt buộc
```

### Phần Mềm Yêu Cầu
```
pandas           >= 1.3.0     # Xử lý dữ liệu
google-search-results >= 2.4.0  # API Google Scholar
xlsxwriter       >= 3.0       # Tạo file Excel
openpyxl         >= 3.0       # Thao tác Excel
python-dotenv    >= 0.21      # Đọc file .env
requests         >= 2.25.0    # HTTP requests
```

---

## 📥 Cài Đặt

### Bước 1: Clone hoặc Tải Dự Án
```bash
# Clone từ Git (nếu có)
git clone <repository-url>
cd Research - Mining

# Hoặc tải file zip trực tiếp
```

### Bước 2: Tạo Virtual Environment (Khuyến Cáo)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies
```bash
# Cài đặt tất cả packages cần thiết
pip install -r requirements.txt

# Nâng cấp pip, setuptools
pip install --upgrade pip setuptools
```

### Bước 4: Kiểm Tra Cài Đặt
```bash
# Kiểm tra imports có thành công không
python -c "from serpapi import GoogleSearch; print('✓ SerpApi installed')"
python -c "import pandas; print('✓ Pandas installed')"

# Chạy help để xem tham số
python main.py --help
```

---

## ⚙️ Cấu Hình

### Bước 1: Tạo File API.env

Dự án bao gồm template file `Data/API.env`. Cần chỉnh sửa:

```bash
# Data/API.env
SERPAPI_KEY=your_actual_api_key_here
OUTPUT_DIR=Data
MIN_CITATIONS=0
API_RATE_LIMIT=1
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

### Bước 2: Lấy SerpApi Key Miễn Phí

1. Truy cập: https://serpapi.com/
2. Đăng ký tài khoản (miễn phí)
3. Đi tới Dashboard → API Key
4. Copy API key 64 ký tự
5. Paste vào `Data/API.env` thay vào `your_actual_api_key_here`

### Bước 3: Bảo Vệ File Cấu Hình

```bash
# Đảm bảo Data/API.env không được commit vào git
# (Đã có trong .gitignore)

# Kiểm tra:
cat .gitignore | grep "API.env"
```

### Các Tùy Chọn Cấu Hình

| Tùy Chọn | Mô Tả | Mặc Định | Phạm Vi |
|---------|-------|---------|--------|
| **SERPAPI_KEY** | API key SerpApi | ❌ Bắt buộc | - |
| **OUTPUT_DIR** | Thư mục output | `Data` | Đường dẫn tuyệt đối |
| **MIN_CITATIONS** | Lọc bài báo có >= citations | `0` | 0-1000+ |
| **API_RATE_LIMIT** | Delay giữa API calls (giây) | `1.0` | 0.5-10.0 |
| **MAX_RETRIES** | Số lần retry tối đa | `3` | 1-10 |
| **REQUEST_TIMEOUT** | Timeout request (giây) | `30` | 10-120 |

---

## 🚀 Hướng Dẫn Sử Dụng

### Chế Độ 1: Tương Tác (Interactive Mode)

```bash
python main.py

# Output:
# 📝 Enter research topic: Deep Learning
# 📅 Filter from year (YYYY) [2020]: 2023
# 🎯 Choose mode (top_tier/all) [top_tier]: all
# 📊 Limit number of papers [40]: 100
```

**Thích hợp cho:** Khám phá nhanh, người dùng muốn kiểm soát từng bước

### Chế Độ 2: Command Line (Fully Automated)

```bash
# Ví dụ 1: Tìm bài báo về Deep Learning từ 2020 (top-tier journals)
python main.py --topic "deep learning" --year 2020 --mode top_tier --limit 50

# Ví dụ 2: Tìm AI papers từ mọi nguồn
python main.py -t "artificial intelligence" -y 2021 -m all -n 100

# Ví dụ 3: Tìm Machine Learning từ tất cả năm và sources
python main.py --topic "machine learning" --mode all --limit 200
```

**Thích hợp cho:** CI/CD pipelines, batch processing, scheduling

### Chế Độ 3: Không Prompt (No Prompt Mode)

```bash
# Chạy mà không có prompts (dùng giá trị mặc định)
python main.py --no_prompt

# Hoặc kết hợp:
python main.py --topic "quantum computing" --no_prompt
```

**Thích hợp cho:** Automated scripts, cron jobs, GitHub Actions

### Các Tùy Chọn Command Line Chi Tiết

```
usage: main.py [-h] [--topic TOPIC] [--year YEAR] [--mode {top_tier,all}]
               [--limit LIMIT] [--no_prompt]

Research Mining Pipeline - Hệ thống khai thác công bố khoa học

optional arguments:
  -h, --help            Hiển thị trợ giúp
  --topic TOPIC, -t TOPIC
                        Chủ đề tìm kiếm (ví dụ: "deep learning")
  --year YEAR, -y YEAR  Năm bắt đầu (default: 2020, phạm vi: 1900-hiện tại)
  --mode {top_tier,all}, -m {top_tier,all}
                        Chế độ:
                        • top_tier: Nature, Science, IEEE, ACM, Cell
                        • all: Tất cả các nguồn
  --limit LIMIT, -n LIMIT
                        Số lượng bài báo tối đa (default: 40, max: 1000)
  --no_prompt           Không hiển thị prompts, dùng default
```

---

## 📁 Cấu Trúc Dự Án

```
Research - Mining/
│
├── 📄 main.py                      # Entry point - Điều phối pipeline
│   ├── validate_inputs()           # Xác thực các tham số
│   ├── parse_args()                # Parse command line arguments
│   └── class Pipeline              # Chạy mining → validating → formatting
│
├── 📁 modules/                     # Core business logic (module hóa)
│   ├── __init__.py
│   ├── mining.py                   # Khai thác từ Google Scholar
│   │   └── class MiningEngine
│   │       ├── extract()           # API chính
│   │       ├── _call_api_with_retry()  # Retry logic
│   │       ├── _parse_metadata()
│   │       ├── _calculate_velocity()
│   │       └── _assign_q_rank()
│   ├── validating.py               # Xác thực & làm sạch dữ liệu
│   │   └── class DataValidator
│   │       ├── validate()          # API chính
│   │       ├── _validate_doi()
│   │       ├── _validate_year()
│   │       └── _validate_citations()
│   ├── formatting.py               # Định dạng & xuất
│   │   └── class DataFormatter
│   │       ├── export_to_excel()   # API chính
│   │       ├── _build_summary()
│   │       └── _build_insights()
│   └── README.md                   # Tài liệu chi tiết các module
│
├── 📁 utils/                       # Utility helpers
│   ├── __init__.py
│   ├── config.py                   # Đọc cấu hình từ .env
│   │   └── load_config()           # API chính
│   ├── logger.py                   # Setup logging
│   │   └── get_logger()            # API chính
│   └── README.md
│
├── 📁 Data/                        # Runtime data & API key
│   ├── API.env                     # 🔐 API KEY (keep PRIVATE!)
│   ├── mining_log.txt             # Log file
│   ├── Executive_Report_*.xlsx    # Output files
│   └── README.md
│
├── 📁 logs/                        # Application logs
│   └── mining_log.txt             # Detailed logs
│
├── 📁 reports/                     # Generated reports
│   └── (Excel files từ formatting)
│
├── 📁 Validate/                    # Validation outputs
│   └── (Reference files)
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # 📖 This file
└── 📄 .env.example                 # Example environment file
```

---

## 🔧 Chi Tiết Các Module

### 1. Module Mining (modules/mining.py)

**Mục đích:** Khai thác dữ liệu công bố khoa học từ Google Scholar

**Class chính:** `MiningEngine`

**Phương thức chính:**
```python
extract(
    query: str,           # Chủ đề tìm kiếm (bắt buộc)
    year_start: int = 2020,  # Năm bắt đầu
    limit: int = 40,      # Số lượng bài báo
    mode: str = "top_tier"  # top_tier hoặc all
) -> pd.DataFrame
```

**Đầu ra DataFrame:**
```
title              : Tiêu đề bài báo (UPPERCASE)
doi                : Digital Object Identifier
q_rank             : Q1/Q2/Q3/Q4 (dựa trên velocity)
access_status      : Open Access (PDF) hoặc Locked/Paywall
year               : Năm xuất bản
authors            : Danh sách tác giả
journal            : Tạp chí/Hội nghị
total_citations    : Tổng số trích dẫn
hotness_v          : Velocity (citations/year)
snippet            : Tóm tắt bài báo
link               : URL đến bài báo
```

**Tính năng:**
- ✅ Retry logic tự động (exponential backoff)
- ✅ Rate limiting có thể cấu hình
- ✅ Error handling toàn diện
- ✅ Logging chi tiết từng API call

### 2. Module Validating (modules/validating.py)

**Mục đích:** Xác thực, làm sạch và chuẩn hóa dữ liệu

**Class chính:** `DataValidator`

**Phương thức chính:**
```python
validate(df: pd.DataFrame) -> pd.DataFrame
```

**Các bước xác thực:**
1. ✅ Xóa khoảng trắng từ các trường string
2. ✅ Chuẩn hóa tiêu đề (UPPERCASE)
3. ✅ Chuẩn hóa tạp chí (Title Case)
4. ✅ Kiểm tra định dạng DOI (regex validation)
5. ✅ Xác thực năm (1900-2100)
6. ✅ Xác thực số trích dẫn (>= 0)
7. ✅ Xóa bản ghi trùng lặp theo tiêu đề
8. ✅ Lọc theo ngưỡng trích dẫn tối thiểu
9. ✅ Reset index

### 3. Module Formatting (modules/formatting.py)

**Mục đích:** Định dạng dữ liệu và xuất báo cáo Excel

**Class chính:** `DataFormatter`

**Phương thức chính:**
```python
export_to_excel(
    df: pd.DataFrame,
    filename: Optional[str] = None
) -> Path
```

**Output Excel (3 sheets):**

**Sheet 1: Executive Summary**
- Tổng số bài báo
- Tổng trích dẫn & trung bình
- Phân bố Q-rank (Q1, Q2, Q3, Q4)
- Tỷ lệ bài báo gần đây
- Độ bao phủ DOI
- **Quality Score (0-100)** dựa trên:
  - Q1/Q2 ratio: 35%
  - Recent papers: 25%
  - DOI coverage: 20%
  - Hotness score: 20%
- Khuyến cáo (High/Good/Moderate)

**Sheet 2: Insights**
- Top 10 tạp chí xuất bản nhiều nhất
- Top 5 bài báo "nóng nhất" (highest velocity)
- Top 5 bài báo được trích dẫn nhiều nhất

**Sheet 3: Clean Data**
- Dữ liệu đầy đủ (11 cột)
- Header frozen (dễ scroll)
- Autofilter enabled
- Auto-fit column width

---

## 📊 Kết Quả Xuất Ra

### Định Dạng File

```
Data/Executive_Report_20260429_203655.xlsx
                     └─ YYYYMMDD_HHMMSS (timestamp)
```

### Nội Dung Excel

**Executive Summary Example:**
| Metric | Value |
|--------|-------|
| Total Papers | 47 |
| Total Citations | 2,341 |
| Average Citations | 49.8 |
| Average Hotness | 8.5 |
| Peak Hotness | 32.1 |
| Q1 Papers | 12 |
| Q2 Papers | 15 |
| High Tier Ratio (Q1+Q2) | 57.45% |
| Recent Papers Ratio (2Y) | 34.04% |
| DOI Coverage | 91.49% |
| **Executive Quality Score** | **78.45** |
| Recommendation | 🟡 Good dataset |

### Logs

**File:** `logs/mining_log.txt`

```
[2026-04-29 20:36:08,258] [INFO] __main__: Pipeline started
[2026-04-29 20:36:08,258] [INFO] __main__: Starting pipeline: topic=machine learning...
[2026-04-29 20:36:10,028] [INFO] MiningEngine: Starting mining: query='machine learning'
[2026-04-29 20:36:12,500] [INFO] MiningEngine: API call successful (attempt 1/3)
[2026-04-29 20:36:12,600] [INFO] MiningEngine: Fetched 20 results at start_idx=0
[2026-04-29 20:36:13,600] [INFO] MiningEngine: Mining complete: extracted 47 records
[2026-04-29 20:36:13,700] [INFO] DataValidator: Validating 47 records
[2026-04-29 20:36:13,750] [INFO] DataValidator: Removed 2 duplicate records
[2026-04-29 20:36:13,800] [INFO] DataValidator: Validation complete: 45 valid records
[2026-04-29 20:36:13,850] [INFO] DataFormatter: Exporting to Data/Executive_Report_*.xlsx
[2026-04-29 20:36:14,000] [INFO] DataFormatter: ✓ Export successful (45 records)
```

---

## 🎓 Các Tính Năng Nâng Cao

### Advanced Usage 1: Batch Processing

```bash
#!/bin/bash
# Chạy nhiều chủ đề
for topic in "deep learning" "machine learning" "NLP" "computer vision"; do
    python main.py --topic "$topic" --year 2023 --limit 100 --no_prompt
done
```

### Advanced Usage 2: Cron Job (Linux/macOS)

```bash
# Chạy hàng ngày lúc 8:00 sáng
0 8 * * * cd /path/to/Research\ -\ Mining && python main.py --topic "AI" --no_prompt

# Cú pháp crontab:
# ┌───────────── phút (0 - 59)
# │ ┌───────────── giờ (0 - 23)
# │ │ ┌───────────── ngày trong tháng (1 - 31)
# │ │ │ ┌───────────── tháng (1 - 12)
# │ │ │ │ ┌───────────── ngày trong tuần (0 - 6) (0=Sunday)
# │ │ │ │ │
# 0 8 * * * <command>
```

### Advanced Usage 3: Task Scheduler (Windows)

```powershell
# Tạo scheduled task
$trigger = New-JobTrigger -Daily -At 8:00AM
$action = New-ScheduledJobOption -RunElevated
$job = Register-ScheduledJob -Name "MiningJob" `
    -Trigger $trigger `
    -ScriptBlock {
        cd "C:\Users\Phamv\Desktop\Research - Mining"
        python main.py --topic "AI" --no_prompt
    }
```

### Advanced Usage 4: Environment Variables

```bash
# Sử dụng environment variables thay vì .env file
export SERPAPI_KEY="your_key_here"
export MIN_CITATIONS=5
export MAX_RETRIES=5
python main.py --topic "deep learning"
```

### Advanced Usage 5: Custom Output Directory

```bash
# Lưu output vào thư mục khác
export OUTPUT_DIR="/path/to/custom/reports"
python main.py --topic "quantum computing" --limit 50
```

---

## 🐛 Xử Lý Lỗi & Khắc Phục

### Lỗi 1: SERPAPI_KEY not configured

**Triệu chứng:**
```
ValueError: SERPAPI_KEY not configured. 
Please set it in Data/API.env or SERPAPI_KEY environment variable
```

**Giải pháp:**
```bash
# 1. Kiểm tra file Data/API.env tồn tại
ls Data/API.env

# 2. Kiểm tra nội dung
cat Data/API.env | grep SERPAPI_KEY

# 3. Lấy key từ https://serpapi.com/
# 4. Edit Data/API.env:
SERPAPI_KEY=your_actual_64_char_key_here

# 5. Test lại
python main.py --help
```

### Lỗi 2: google-search-results package not available

**Triệu chứng:**
```
RuntimeError: serpapi package not available in the environment.
```

**Giải pháp:**
```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt

# Hoặc cài trực tiếp:
pip install google-search-results>=2.4.0
```

### Lỗi 3: No results found

**Triệu chứng:**
```
⚠️  No results found for this query. Try different keywords or relaxed filters.
```

**Nguyên nhân & Giải pháp:**
```bash
# 1. Chủ đề quá cụ thể: Dùng keywords chung chung
❌ python main.py --topic "Quantum Entanglement in Boson Sampling"
✅ python main.py --topic "quantum computing"

# 2. Year filter quá mới: Bài báo mới chưa được index
❌ python main.py --year 2026 --limit 100
✅ python main.py --year 2023 --limit 100

# 3. Top-tier filter quá hạn chế: Thử --mode all
❌ python main.py --topic "my-topic" --year 2024 --mode top_tier
✅ python main.py --topic "my-topic" --year 2024 --mode all
```

### Lỗi 4: Input validation error

**Triệu chứng:**
```
❌ Topic must be at least 2 characters long
❌ Year must be >= 1900
❌ Limit must be <= 1000
```

**Giải pháp:**
```bash
# ✅ Valid inputs:
python main.py --topic "AI" --year 2020 --limit 50

# ❌ Invalid:
python main.py --topic "A"            # Quá ngắn
python main.py --year 1800            # Quá cũ
python main.py --limit 1001           # Quá nhiều
```

---

## 📋 FAQ & Hỏi Đáp

### Q1: SerpApi có miễn phí không?

**A:** Có, SerpApi cung cấp gói miễn phí:
- **100 queries/tháng** (miễn phí)
- Sau đó: ~$0.05/query
- Đăng ký: https://serpapi.com/pricing

### Q2: Tôi có thể chạy chương trình này offline không?

**A:** Không, cần internet vì API lấy dữ liệu từ Google Scholar qua SerpApi.

### Q3: Nếu API key hết quota thì sao?

**A:** Chương trình sẽ báo lỗi "API key not valid or has exceeded the monthly rate limit"

**Giải pháp:**
1. Nâng cấp gói SerpApi (https://serpapi.com/)
2. Chờ tháng tới để reset quota miễn phí
3. Sử dụng key từ tài khoản khác

### Q4: Chất lượng dữ liệu bao nhiêu?

**A:** Phụ thuộc vào:
- Số lượng kết quả trả về từ API
- Định dạng metadata của bài báo
- Chỉ lấy những bài báo Google Scholar indexed

### Q5: Tôi có thể modify chương trình không?

**A:** Có, chương trình là open-source. Bạn có thể:
- Modify bất kỳ module nào
- Thêm features mới
- Custom output format
- Integrate vào hệ thống khác

### Q6: Excel report có thể import vào Excel từ định dạng khác không?

**A:** Có thể thêm format khác (CSV, JSON) bằng cách modify `modules/formatting.py`

### Q7: Làm sao để tăng tốc độ?

**A:** 
```bash
# 1. Giảm limit (ít request)
python main.py --topic "AI" --limit 10

# 2. Tăng rate limit (careful - có thể bị rate limit)
# Edit Data/API.env:
API_RATE_LIMIT=0.5   # 0.5 giây thay vì 1 giây

# 3. Sử dụng mode top_tier (ít kết quả)
python main.py --topic "AI" --mode top_tier
```

### Q8: Log file ở đâu?

**A:** 
```bash
# File log chi tiết:
logs/mining_log.txt

# Xem log real-time:
tail -f logs/mining_log.txt  # Linux/macOS
Get-Content -Tail 50 logs/mining_log.txt  # Windows PowerShell
```

### Q9: Tôi có thể cấu hình lại DOI regex không?

**A:** Có, edit file `modules/mining.py` tìm `_parse_metadata()`:
```python
doi_pattern = r"10\.\d{4,9}/[-._;()/:\w]+"  # Regex DOI
```

### Q10: Nếu Git ở đâu để submit issues?

**A:** Hãy tạo issue trên GitHub repo (nếu có) hoặc liên hệ tác giả trực tiếp.

---

## 📈 Hiệu Suất & Benchmark

### Benchmark Typical Performance

```
Query:  "machine learning"
Mode:   all
Year:   2020
Limit:  100 papers

Results:
✓ Mining phase:       8-12 seconds
✓ Validation phase:   0.5-1 second
✓ Formatting phase:   1-2 seconds
─────────────────────────────────────
Total time:           10-15 seconds
Memory usage:         150-300 MB
Output file size:     500 KB - 2 MB
```

### Optimization Tips

1. **Giảm limit** để tăng tốc độ
   ```bash
   python main.py --topic "AI" --limit 10  # 5-8 giây
   ```

2. **Sử dụng top_tier mode** (ít kết quả)
   ```bash
   python main.py --topic "AI" --mode top_tier  # 6-10 giây
   ```

3. **Batch processing** với nhiều queries
   ```bash
   for q in "AI" "ML" "DL"; do
     python main.py --topic "$q" --limit 50 &  # Run parallel
   done
   ```

---

## 🤝 Đóng Góp & Phát Triển

### Cách Contribute

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Setup

```bash
# Clone & setup
git clone <your-fork>
cd Research - Mining
python -m venv venv
venv/Scripts/activate  # or source venv/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black .
isort .
pylint modules/
```

### Code Style

- **Python style**: PEP 8
- **Type hints**: Required
- **Docstrings**: Google style
- **Logging**: Use logger from utils.logger

---

## 📞 Support & Liên Hệ

| Vấn đề | Giải pháp |
|--------|----------|
| 🐛 Bug report | GitHub Issues |
| 💡 Feature request | GitHub Discussions |
| ❓ Câu hỏi | GitHub Q&A |
| 📧 Email | contact@example.com |

---

## 📜 Giấy Phép

MIT License - Xem [LICENSE](LICENSE) file

---

## ⭐ Changelog

### v2.0.0 (2026-04-29) - Current
- ✅ Refactored to modular architecture
- ✅ Added comprehensive error handling
- ✅ Added input validation
- ✅ Added retry logic with exponential backoff
- ✅ Enhanced Excel export with insights
- ✅ Improved logging & documentation
- ✅ Vietnamese README

### v1.0.0 (Initial Release)
- ✅ Basic mining functionality
- ✅ Simple validation
- ✅ Excel export

---

## 🙏 Cảm Ơn

Cảm ơn tất cả những người đã sử dụng và đóng góp cho dự án này!

---

**📖 Trang cuối cùng cập nhật:** 2026-04-29  
**👤 Tác giả:** Research Mining Team  
**🌐 Repository:** [GitHub URL]  
**📧 Email:** support@researchmining.dev