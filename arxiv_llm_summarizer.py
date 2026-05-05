import sys
import os

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import psycopg2
import time

# ---------------- CẤU HÌNH LLM ----------------
# ĐIỀN API KEY CỦA BẠN VÀO ĐÂY
API_KEY = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')

POSTGRES_SERVER=os.getenv('POSTGRES_SERVER', 'localhost')
POSTGRES_PORT=int(os.getenv('POSTGRES_PORT', '5432'))
POSTGRES_DB=os.getenv('POSTGRES_DB', 'arxiv_db')
POSTGRES_USER=os.getenv('POSTGRES_USER', 'arxiv_user')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD', 'arxiv_password')

# ---------------- CẤU HÌNH DATABASE ----------------
DB_PARAMS = {
    'dbname': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'host': POSTGRES_SERVER,
    'port': POSTGRES_PORT
}


def init_db():
    """Kết nối database và tạo bảng nếu chưa tồn tại."""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    create_table_query = """
                         CREATE TABLE IF NOT EXISTS papers \
                         ( \
                             id \
                             SERIAL \
                             PRIMARY \
                             KEY, \
                             title \
                             TEXT \
                             NOT \
                             NULL, \
                             authors \
                             TEXT, \
                             published_date \
                             VARCHAR \
                         ( \
                             50 \
                         ),
                             link TEXT UNIQUE NOT NULL,
                             abstract TEXT,
                             summary_vi TEXT
                             ); \
                         """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Đã kiểm tra/khởi tạo Database thành công.")


def fetch_arxiv_recent_ai(max_results=10):
    """Sử dụng ArXiv API để fetch các bài báo mới nhất thuộc danh mục Machine Learning."""
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': 'all:"machine learning"',
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'max_results': max_results
    }

    print(f"Đang lấy {max_results} bài báo ML mới nhất từ ArXiv API...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
        summary = entry.find('atom:summary', ns).text.replace('\n', ' ').strip()
        link = entry.find('atom:id', ns).text

        raw_date = entry.find('atom:published', ns).text
        try:
            dt = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
            published_date = dt.strftime("%d/%m/%Y")
        except ValueError:
            published_date = raw_date

        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]

        papers.append({
            'title': title,
            'authors': ', '.join(authors),
            'published_date': published_date,
            'abstract': summary,
            'link': link
        })

    return papers


def summarize_with_llm(abstract):
    """Nhúng LLM bằng cách gọi trực tiếp REST API của Gemini (Fix lỗi thư viện trên Windows)."""
    prompt = (
        "Bạn là một chuyên gia về Khoa học Máy tính và AI. Hãy đọc phần tóm tắt (Abstract) "
        "của bài báo khoa học sau đây và viết lại thành 1 đoạn tổng quan duy nhất bằng tiếng Việt, "
        "nêu bật bài toán họ giải quyết và phương pháp/kết quả chính. Trình bày súc tích, dễ hiểu:\n\n"
        f"{abstract}"
    )

#     curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
#   -H "x-goog-api-key: $GEMINI_API_KEY" \
#   -H 'Content-Type: application/json' \
#   -X POST \
#   -d '{
#     "contents": [
#       {
#         "parts": [
#           {
#             "text": "Explain how AI works in a few words"
#           }
#         ]
#       }
#     ]
#   }'
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': API_KEY
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text']
        return summary.strip()
    except Exception as e:
        return f"[Lỗi REST API Gemini]: {str(e)}"


def save_to_db(paper_data):
    """Lưu 1 bài báo vào Database."""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    insert_query = """
                   INSERT INTO papers (title, authors, published_date, link, abstract, summary_vi)
                   VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (link) DO NOTHING; \
                   """

    cursor.execute(insert_query, (
        paper_data['title'],
        paper_data['authors'],
        paper_data['published_date'],
        paper_data['link'],
        paper_data['abstract'],
        paper_data['summary_vi']
    ))

    is_inserted = cursor.rowcount > 0
    conn.commit()
    cursor.close()
    conn.close()

    return is_inserted


def main():
    # 1. Khởi tạo Database
    init_db()

    # 2. Lấy dữ liệu (Chỉnh số lượng ở đây)
    papers = fetch_arxiv_recent_ai()

    print("\n" + "=" * 80)
    for i, paper in enumerate(papers, 1):
        print(f"BÀI {i}: {paper['title']}")
        print("Trạng thái: Đang tạo tóm tắt tiếng Việt bằng LLM...")

        # Gọi LLM
        summary_vi = summarize_with_llm(paper['abstract'])
        paper['summary_vi'] = summary_vi
        print("Trạng thái: Đang lưu vào Database...")

        # Lưu DB
        inserted = save_to_db(paper)

        if inserted:
            print("=> Đã lưu thành công vào PostgreSQL!")
        else:
            print("=> Bài báo này đã tồn tại trong DB, tự động bỏ qua.")

        print("-" * 40)
        # if i < len(papers):
        #     print(f"⏳ Đang nghỉ 15 giây để tránh quá tải API...")
        #     time.sleep(15)


if __name__ == '__main__':
    main()