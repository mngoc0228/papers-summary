# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from src.routes.auth.auth_routes import auth_route 

app = FastAPI(
    title="Hệ thống Theo dõi & Tóm tắt Paper API",
    description="API cho ứng dụng đọc báo khoa học tự động tóm tắt",
    version="1.0.0"
)

app.include_router(auth_route)


@app.get("/")
async def root():
    return {"message": f"Hello World! Welcome to Paper Tracker API"}

# # --- 1. SCHEMAS (Định dạng dữ liệu trả về/nhận vào) ---
# class TopicCreate(BaseModel):
#     name: str

# class PaperResponse(BaseModel):
#     id: int
#     title: str
#     author: str
#     abstract: str
#     summary: str | None = None
#     published_date: str
#     link: str

# # --- 2. NLP SUMMARIZATION (Giả lập) ---
# def generate_summary(abstract: str) -> str:
#     # TODO: Tích hợp gọi API Gemini/OpenAI tại đây
#     return "Đây là câu tóm tắt tự động được sinh ra từ Abstract dài..."

# # --- 3. API ENDPOINTS ---

# # --- Papers ---
# @app.get("/papers", response_model=list[PaperResponse], tags=["Papers"])
# def get_papers(topic: str = None, keyword: str = None):
#     # TODO: Query database PostgreSQL để lấy danh sách papers. Lọc theo topic/keyword nếu có.
#     return [
#         {
#             "id": 1,
#             "title": "Attention Is All You Need",
#             "author": "Ashish Vaswani et al.",
#             "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
#             "summary": "Mô hình Transformer sử dụng cơ chế Attention giúp loại bỏ mạng RNN/CNN, tăng tốc độ huấn luyện.",
#             "published_date": "2017-06-12",
#             "link": "https://arxiv.org/abs/1706.03762"
#         }
#     ]

# @app.get("/papers/{paper_id}", response_model=PaperResponse, tags=["Papers"])
# def get_paper_detail(paper_id: int):
#     # TODO: Query chi tiết 1 paper
#     pass

# # --- Topics ---
# @app.post("/topics", tags=["Topics"])
# def add_topic(topic: TopicCreate):
#     # TODO: Lưu chủ đề user muốn theo dõi vào bảng Topics
#     return {"message": f"Đã thêm chủ đề: {topic.name}"}

# # --- Favorites ---
# @app.post("/favorites/{paper_id}", tags=["Favorites"])
# def add_favorite(paper_id: int):
#     # TODO: Lưu paper_id vào bảng Favorites của User hiện tại
#     return {"message": "Đã lưu bài báo vào danh sách yêu thích!"}