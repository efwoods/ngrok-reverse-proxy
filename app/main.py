import asyncio
from fastapi import FastAPI
from services.get_ngrok_client import get_ngrok_client  # Adjust import path accordingly
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        public_url = await get_ngrok_client()
        app.state.ngrok_url = public_url
        print(f"Ngrok tunnel started at: {public_url}")
        yield
    except Exception as e:
        print(f"Error starting ngrok tunnel: {e}")
        raise

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return RedirectResponse(url="/healthy")

@app.get("/healthy")
async def healthy():
    return {
        "message": "Healthy", 
        "ngrok_url": getattr(app.state, "ngrok_url", None)
    }
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 