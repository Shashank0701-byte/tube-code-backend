from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from extractor import get_video_transcript
from ai_agent import clean_code_with_ai
import re

app = FastAPI()

# 1. Allow the Extension to talk to us (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

def extract_video_id(url):
    # Regex to find the 'v=' part of a YouTube URL
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    # Handle 'youtu.be/' short links
    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

@app.post("/get-code")
def get_code(request: VideoRequest):
    print(f"📥 Received Request for: {request.url}")
    
    # 1. Get Video ID
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # 2. Get Raw Transcript (The Messy Text)
    raw_text = get_video_transcript(video_id)
    if "Error" in raw_text:
        raise HTTPException(status_code=500, detail=raw_text)

    # 3. Clean it with AI (The Magic)
    clean_code = clean_code_with_ai(raw_text)
    
    return {"code": clean_code}