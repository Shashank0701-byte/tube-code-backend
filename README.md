# Tube-Code

Tube-Code is a local-first browser extension that uses AI to extract runnable code snippets directly from YouTube video transcripts. It eliminates the need to pause, switch tabs, and manually type code while watching tutorials.

## The Problem
Learning from video tutorials introduces a "Context Switching Tax." Developers spend nearly 40% of their learning time pausing videos and transcribing code manually. This friction breaks focus and slows down the learning process.

## The Solution
Tube-Code runs a lightweight Python server on your local machine that:
1.  Intercepts the video ID from the browser extension.
2.  Uses `yt-dlp` to fetch the raw transcript (bypassing cloud IP blocks).
3.  Processes the text using Google's Gemini 1.5 Flash model to identify and clean Python syntax.
4.  Returns formatted, runnable code directly to your clipboard.

## Architecture

* **Client:** Chrome Extension (Manifest V3) injecting a native-feeling button into the YouTube UI.
* **Server:** FastAPI (Python) running locally to handle request processing.
* **Extraction:** `yt-dlp` for robust subtitle retrieval.
* **Intelligence:** Google Gemini 1.5 Flash for Natural Language Processing (cleaning conversational filler).

## Installation

Since this tool bypasses YouTube's bot detection by running on your residential IP, it requires a simple local setup.

### Prerequisites
* Python 3.10+
* Google Gemini API Key (Free)

### 1. Setup the Backend (The Brain)

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/tube-code.git](https://github.com/YOUR_USERNAME/tube-code.git)
cd tube-code/backend

# Install dependencies
pip install -r requirements.txt

# Configure API Key
# Create a .env file and add: GEMINI_API_KEY=your_key_here
echo "GEMINI_API_KEY=AIzaSy..." > .env

# Start the server
uvicorn main:app --reload