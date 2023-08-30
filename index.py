from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers.router import router 
app = FastAPI()
app.include_router(router)

@app.get("/")
async def get_upload_page():
    return FileResponse("index.html")