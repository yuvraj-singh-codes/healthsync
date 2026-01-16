from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data model
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Create item endpoint
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)