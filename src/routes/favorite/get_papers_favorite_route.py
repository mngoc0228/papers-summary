from src.routes.favorite import router

@router.get("")
async def get_papers_favorite(
    id: str,
):
    return {"message": "Get a paper favorite", "data": [{"id": "1", "user_id": "123", "paper_id": id}]}