# DataMine Framework V3

> Lightweight Data Mining & Web Reconnaissance Framework built with Python.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

# Overview

DataMine Framework V3 là một dự án Python tập trung vào:
- Web Data Mining
- Table Extraction
- Email Mining
- Lightweight OSINT
- Semi-structured Data Processing

Mục tiêu của dự án là xây dựng một framework nhỏ gọn nhưng có khả năng:
- tự động quét dữ liệu website,
- trích xuất bảng dữ liệu,
- mining email,
- export dữ liệu đa định dạng,
- và tạo nền tảng cho các hệ thống Data Engineering / OSINT lớn hơn trong tương lai.

---

# Main Features

## Automatic Table Mining
- Tự động phát hiện tất cả bảng HTML
- Làm sạch dữ liệu tự động
- Ranking bảng theo độ quan trọng
- Export CSV & Excel

---

## Email Mining
- Quét email từ toàn bộ website
- Loại bỏ duplicate
- Làm sạch HTML trước khi mining
- Export danh sách email

---

## Smart Data Cleaning
- Loại bỏ:
  - script
  - style
  - noscript
- Chuẩn hóa dữ liệu đầu vào

---

## Logging System
- Theo dõi:
  - kết nối
  - lỗi hệ thống
  - trạng thái mining
- Hỗ trợ debugging & monitoring

---

## Multi-format Export
Hỗ trợ:
- CSV
- Excel (.xlsx)

---

## Modular Architecture
Tách module riêng biệt:
- scraper
- miner
- exporter
- cleaner
- logger

Giúp dễ:
- mở rộng
- bảo trì
- scale dự án

---

# Project Structure

```bash
DataMine/
│
├── core/
│   ├── scraper.py
│   ├── table_miner.py
│   ├── email_miner.py
│   ├── exporter.py
│   ├── cleaner.py
│   └── logger.py
│
├── outputs/
│
├── logs/
│
├── requirements.txt
│
└── main.py
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/DataMine.git
cd DataMine
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```txt
pandas
requests
beautifulsoup4
lxml
openpyxl
rich
```

---

# Usage

## Run Application

```bash
python main.py
```

---

## Example Workflow

```text
===> DataMine Framework V3 <===

Enter target URL:
https://example.com
```

---

## Available Functions

| Option | Description |
|---|---|
| 1 | Mine all tables |
| 2 | Mine emails |
| 3 | Full scan |
| 4 | Exit |

---

# Outputs

## Exported Tables

```bash
outputs/
├── table_1.csv
├── table_2.csv
└── all_tables.xlsx
```

---

## Exported Emails

```bash
outputs/emails.csv
```

---

# Logging

Logs được lưu tại:

```bash
logs/datamine.log
```

Ví dụ:

```text
2026-05-07 10:12:03 - INFO - Connecting to: https://example.com
2026-05-07 10:12:05 - INFO - Found 5 tables
2026-05-07 10:12:06 - INFO - Found 12 emails
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Language |
| Pandas | Data Processing |
| Requests | HTTP Client |
| BeautifulSoup4 | HTML Parsing |
| OpenPyXL | Excel Export |
| Rich | CLI UI |
| Regex | Pattern Matching |

---

# Future Improvements

## Planned Features

### Web Crawling
- Recursive crawling
- Pagination detection
- Internal link discovery

### Browser Automation
- Selenium integration
- Playwright integration
- JavaScript rendering

### Advanced Mining
- Phone number extraction
- Social media extraction
- API key detection
- Metadata mining

### Performance
- Multi-threading
- Async crawling
- Proxy rotation

### Data Engineering
- SQLite backend
- JSON export
- Parquet export
- ETL pipeline support

### AI Integration
- AI table classification
- Content summarization
- Intelligent ranking

### OSINT Features
- WHOIS lookup
- DNS enumeration
- Subdomain scanning

---

# Educational Purpose

Dự án được xây dựng với mục tiêu:
- học tập,
- nghiên cứu cá nhân,
- thực hành Data Mining,
- thực hành Web Scraping,
- nghiên cứu kiến trúc hệ thống dữ liệu.

---

# Legal & Ethical Notice

DataMine Framework chỉ nên được sử dụng cho:
- mục đích giáo dục,
- nghiên cứu,
- kiểm thử hợp pháp,
- hoặc các website được phép truy cập.

Người dùng chịu hoàn toàn trách nhiệm cho việc sử dụng công cụ này.

---

# Contributing

Contributions are welcome.

Bạn có thể:
- mở issue
- gửi pull request
- đề xuất tính năng mới
- cải thiện performance

---

# Author

Developed by: Your Name

---

# License

MIT License

---

# Final Notes

DataMine Framework V3 không chỉ là một script scraping đơn giản.

Đây là nền tảng đầu tiên để phát triển:
- mini data engineering system,
- lightweight OSINT toolkit,
- hoặc scalable mining platform trong tương lai.