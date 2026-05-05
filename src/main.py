from fastapi import FastAPI
from src.routes.auth.auth_routes import auth_route 
from src.routes.favorite.favorite_routes import favorite_route
from src.routes.user.user_routes import user_route
from src.routes.paper.paper_routes import paper_route

app = FastAPI(
    title="Hệ thống Theo dõi & Tóm tắt Paper API",
    description="API cho ứng dụng đọc báo khoa học",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(auth_route)
app.include_router(favorite_route)
app.include_router(user_route)
app.include_router(paper_route)


@app.get("/")
async def root():
    return {"message": f"Hello World! Welcome to Paper Tracker API"}
