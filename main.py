from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hot_wheels_matcher import process_hotwheels_image

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3000",  # Assuming your Next.js app runs on this origin
    # Add any other origins you need
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageUrl(BaseModel):
    url: str

@app.post("/process_image")
async def process_image(image: ImageUrl):
    try:
        result = process_hotwheels_image(image.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))