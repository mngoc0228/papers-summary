# Using uvicorn to run the FastAPI application

import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="localhost", port=int(os.getenv("PORT", 8000)), env_file=".env", reload=True)
