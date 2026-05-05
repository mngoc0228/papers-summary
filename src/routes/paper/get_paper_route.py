from src.routes.paper import router

@router.get('/{id}')
async def get_paper(
    id: str,
):
    return {"message": "Get a paper favorite", "data": {"id": id, "title": "Example Paper Title", "authors": ["Author A", "Author B"], "abstract": "This is an example abstract for the paper."}}