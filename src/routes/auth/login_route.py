from src.routes.auth import router

@router.post(
    '/login',
)
async def login():
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}
