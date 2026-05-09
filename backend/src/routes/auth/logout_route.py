from src.routes.auth import router

@router.post(
    '/logout',
)
async def logout():
    return {"message": "Successfully logged out"}

