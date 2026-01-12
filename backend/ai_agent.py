import google.generativeai as genai
import os
from dotenv import load_dotenv
from extractor import get_video_transcript # Import your tool from Step 2

# 1. Load the API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ API Key not found! Check your .env file.")

genai.configure(api_key=api_key)

# 2. Setup the Model (Gemini 2.5 Flash is fast & cheap)
model = genai.GenerativeModel('gemini-2.5-flash')

def clean_code_with_ai(raw_text):
    print("🤖 AI is reading the transcript...")
    
    # 3. The Prompt Engineering (The most important part)
    prompt = f"""
    You are a Senior Python Developer. 
    I have a raw transcript from a coding tutorial video. 
    It is full of conversational filler ("um", "guys", "subscribe").
    
    YOUR GOAL: Extract ONLY the valid, runnable Python code from this text.
    
    RULES:
    1. Do NOT include any explanations, comments, or conversational text.
    2. Do NOT use markdown code blocks (```python). Just raw text.
    3. If the code is fragmented, fix the indentation and syntax to make it runnable.
    4. If there are multiple snippets, separate them with two newlines.
    
    RAW TRANSCRIPT:
    {raw_text[:30000]}  # Limit to 30k chars to be safe, though Flash handles more
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

if __name__ == "__main__":
    # The Full Flow Test
    video_id = "kqtD5dpn9C8" # Python for Beginners
    
    print(f"1. Fetching Transcript for {video_id}...")
    transcript = get_video_transcript(video_id)
    
    # Check if extractor failed before sending to AI
    if "Error" in transcript:
        print(transcript)
    else:
        print(f"   (Got {len(transcript)} characters of text)")
        
        # Run the AI
        clean_code = clean_code_with_ai(transcript)
        
        print("\n" + "="*40)
        print("   🐍 GENERATED CODE 🐍")
        print("="*40)
        print(clean_code)
        print("="*40)