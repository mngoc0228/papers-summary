from src.routes.paper import router

@router.get('')
async def get_papers(
    id: str,
):
    return {
        "message": "Get list of papers",
        "data": [
            {"id": "1", "title": "Example Paper Title 1", "authors": ["Author A", "Author B"], "abstract": "This is an example abstract for the paper."},
            {"id": "2", "title": "Example Paper Title 2", "authors": ["Author C", "Author D"], "abstract": "This is another example abstract for the paper."}
        ]
    }