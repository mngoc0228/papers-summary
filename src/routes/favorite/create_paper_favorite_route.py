from src.routes.favorite import router

@router.post("")
async def create_paper_favorite(
    id: str,
):
    return {"message": "Create a paper favorite"}